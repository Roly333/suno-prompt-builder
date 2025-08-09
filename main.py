# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.utils import platform

class MainLayout(BoxLayout):
    prompt_output = StringProperty('')
    structure_initialized = BooleanProperty(False)
    selected_structure_item = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.influence_checkboxes, self.enhancement_checkboxes, self.vocalists_data = {}, {}, []
        self.populate_influences()
        self.populate_enhancements()
        self.populate_structure_blocks()
        
        # Bind events directly in Python for reliability
        self.ids.influences_toggle.ids.checkbox.bind(active=self.update_prompt)
        self.ids.vocalists_toggle.ids.checkbox.bind(active=self.toggle_vocalists)
        self.ids.structure_toggle.ids.checkbox.bind(active=self.toggle_structure)
        self.ids.enhancements_toggle.ids.checkbox.bind(active=self.update_prompt)

        self.update_prompt()

    def populate_influences(self):
        container = self.ids.influences_grid
        for tag in App.get_running_app().influence_tags:
            box = BoxLayout(size_hint_y=None, height=dp(30))
            cb = CheckBox(size_hint_x=None, width=dp(48)); cb.bind(active=self.update_prompt)
            label = Label(text=tag, halign='left', valign='middle', font_size='16sp'); label.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)))
            box.add_widget(cb); box.add_widget(label)
            container.add_widget(box)
            self.influence_checkboxes[tag] = cb

    def populate_enhancements(self):
        container = self.ids.enhancements_grid
        for tag in App.get_running_app().enhancement_tags:
            box = BoxLayout(size_hint_y=None, height=dp(30))
            cb = CheckBox(size_hint_x=None, width=dp(48), active=(tag in App.get_running_app().default_enhancements))
            cb.bind(active=self.update_prompt)
            label = Label(text=tag, halign='left', valign='middle', font_size='16sp'); label.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)))
            box.add_widget(cb); box.add_widget(label)
            container.add_widget(box)
            self.enhancement_checkboxes[tag] = cb

    def populate_structure_blocks(self):
        container = self.ids.available_structure_list
        for tag in App.get_running_app().structure_tags:
            btn = Button(text=tag, size_hint_y=None, height=dp(36)); btn.bind(on_release=self.add_to_structure)
            container.add_widget(btn)

    def update_prompt(self, *args):
        prompt_lines = []
        if self.ids.genre_spinner.text:
            prompt_lines.append(f"[{self.ids.sub_genre_spinner.text + ' ' if self.ids.sub_genre_spinner.text else ''}{self.ids.genre_spinner.text}]")
        if self.ids.tempo_input.text.isdigit():
            prompt_lines.append(f"[Tempo {self.ids.tempo_input.text}bpm]")
        tags = [s.text for s in [self.ids.atmos1_spinner, self.ids.atmos2_spinner, self.ids.mood1_spinner, self.ids.mood2_spinner] if s.text]
        if tags:
            prompt_lines.append(" ".join(f"#{tag}" for tag in tags))
        bass_string = f"{self.ids.sub_type_spinner.text} {self.ids.bass_type_spinner.text}".strip()
        if bass_string:
            prompt_lines.append(f"[{bass_string} Bass]")
        if self.ids.break_type_spinner.text:
            prompt_lines.append(f"[{self.ids.break_type_spinner.text} Breaks]")
        if self.ids.drum_type_spinner.text:
            prompt_lines.append(f"[{self.ids.drum_type_spinner.text} Drums]")
        if self.ids.influences_toggle.ids.checkbox.active:
            for tag, cb in self.influence_checkboxes.items():
                if cb.active:
                    prompt_lines.append(f"[{tag}]")
        if self.ids.vocalists_toggle.ids.checkbox.active:
            for i, data in enumerate(self.vocalists_data):
                parts = [s.text for s in data['spinners'].values() if s.text]
                if parts:
                    prompt_lines.append(f"[Vocalist {i+1}: {' '.join(parts)}]")
        if self.ids.structure_toggle.ids.checkbox.active:
            structure_list = [child.text for child in reversed(self.ids.user_structure_list.children)]
            if structure_list:
                if prompt_lines:
                    prompt_lines.append("")
                prompt_lines.extend(structure_list)
        if self.ids.enhancements_toggle.ids.checkbox.active:
            if prompt_lines:
                prompt_lines.append("")
            for tag, cb in self.enhancement_checkboxes.items():
                if cb.active:
                    prompt_lines.append(tag)
        self.prompt_output = "\n".join(prompt_lines)

    def add_vocalist(self):
        container = self.ids.vocalists_container
        v_num = len(self.vocalists_data) + 1
        app = App.get_running_app()
        v_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(314), padding=dp(10), spacing=dp(5))
        header = BoxLayout(size_hint_y=None, height=dp(30))
        header.add_widget(Label(text=f"Vocalist {v_num}", bold=True))
        remove_btn = Button(text="Remove", size_hint_x=None, width=dp(100))
        header.add_widget(remove_btn)
        v_box.add_widget(header)
        data = {'spinners': {}}
        opts = {'Gender': app.gender_options, 'Accent': app.accent_options, 'Style': app.vocal_style_options, 'Delivery': app.delivery_options, 'Delivery 2': app.delivery_options, 'Emotion': app.emotion_options}
        for key, values in opts.items():
            h_box = BoxLayout(size_hint_y=None, height=dp(44))
            h_box.add_widget(Label(text=key, size_hint_x=0.4, font_size='16sp'))
            s = Spinner(text='', values=values, size_hint_x=0.6)
            s.bind(text=self.update_prompt)
            data['spinners'][key] = s
            h_box.add_widget(s)
            v_box.add_widget(h_box)
        data['main_widget'] = v_box
        self.vocalists_data.append(data)
        container.add_widget(v_box)
        remove_btn.bind(on_release=lambda x: self.remove_vocalist(data))
        self.update_prompt()

    def remove_vocalist(self, vocalist_data):
        self.ids.vocalists_container.remove_widget(vocalist_data['main_widget'])
        self.vocalists_data.remove(vocalist_data)
        self.update_prompt()

    def toggle_vocalists(self, checkbox, value):
        if value and not self.vocalists_data:
            self.add_vocalist()
        elif not value:
            self.ids.vocalists_container.clear_widgets()
            self.vocalists_data.clear()
        self.update_prompt()

    def toggle_structure(self, checkbox, value):
        if value and not self.structure_initialized:
            self.ids.user_structure_list.clear_widgets()
            for tag in App.get_running_app().default_song_structure:
                btn = Button(text=tag, size_hint_y=None, height=dp(36))
                btn.bind(on_release=self.select_structure_item)
                self.ids.user_structure_list.add_widget(btn)
            self.structure_initialized = True
        self.update_prompt()

    def add_to_structure(self, instance):
        btn = Button(text=instance.text, size_hint_y=None, height=dp(36))
        btn.bind(on_release=self.select_structure_item)
        self.ids.user_structure_list.add_widget(btn)
        self.update_prompt()

    def select_structure_item(self, instance):
        if self.selected_structure_item:
            self.selected_structure_item.background_color = [1, 1, 1, 1]
        self.selected_structure_item = instance
        self.selected_structure_item.background_color = [0.2, 0.6, 1, 1]

    def move_structure_item(self, direction):
        if not self.selected_structure_item:
            return
        children = list(reversed(self.ids.user_structure_list.children))
        try:
            index = children.index(self.selected_structure_item)
        except ValueError:
            return
        if direction == 'up' and index > 0:
            swap_index = index - 1
            children[index].text, children[swap_index].text = children[swap_index].text, children[index].text
            self.select_structure_item(children[swap_index])
        elif direction == 'down' and index < len(children) - 1:
            swap_index = index + 1
            children[index].text, children[swap_index].text = children[swap_index].text, children[index].text
            self.select_structure_item(children[swap_index])
        self.update_prompt()

    def copy_to_clipboard(self):
        Clipboard.copy(self.prompt_output)
    
    # --- MODIFICATION: Robust file saving with permission handling ---
    def save_to_file(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            def after_permission_request(permissions, grants):
                if all(grants):
                    self._save_file()
                else:
                    self.show_popup("Permission Denied", "Cannot save file without storage permission.")
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE], after_permission_request)
        else:
            self._save_file()

    def _save_file(self):
        try:
            from kivy.app import App
            from os.path import join
            
            # This path is accessible via the phone's file browser
            from android.storage import primary_external_storage_path
            dir = primary_external_storage_path()
            filepath = join(dir, 'Download', 'suno_prompt.txt')

            with open(filepath, "w") as f:
                f.write(self.prompt_output)
            
            self.show_popup("Success", f"Prompt saved to your Downloads folder as suno_prompt.txt")
        except Exception as e:
            self.show_popup("Error", f"Failed to save file: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()


class PromptBuilderApp(App):
    # Data lists...
    genre_options = ["", "DnB", "Ambient", "Jungle"]; sub_genre_options = ["", "Neuro", "Technical", "Minimal", "Liquid", "Jump Up", "Deep", "Raw", "1990's"]
    bass_type_options = ["", "Reese", "Growl", "FM", "Wobble", "Morphing", "Filtered", "Granular", "Modulated"]; drum_type_options = ["", "Rolling", "Technical", "Complex", "Stepped", "Machine", "Crushed", "Layered", "Processed"]
    break_type_options = ["", "Amen", "Think", "Apache", "Pitched", "Chopped", "Reversed", "Stacked", "Micro"]; sub_type_options = ["", "Clean", "Moving", "Pulsing", "Heavy", "Warm", "Deep", "Distorted", "Square"]
    atmosphere_options = ["", "Industrial", "Mechanical", "Ethereal", "Dystopian", "Cinematic", "Spacious", "Underground", "Metallic"]; mood_options = ["", "Dark", "Aggressive", "Raw", "Mysterious", "Intense", "Clinical", "Polished", "Minimal"]
    gender_options = ["", "Male", "Female", "Non-binary"]; accent_options = ["", "UK London", "UK Birmingham", "UK Liverpool", "UK Manchester", "UK Leeds", "UK Bristol", "American", "Caribbean", "African", "European"]
    delivery_options = ["", "Smooth", "Raspy", "Energetic", "Fast", "Rhythmic", "Spoken Word", "Drawled", "Melodic", "Soulful", "Hype", "Call and Response", "Freestyle", "Crowd Interaction", "Adlib"]; emotion_options = ["", "Happy", "Sad", "Angry", "Confident", "Raw", "Intense", "Chill", "Aggressive", "Hypnotic", "Dark", "Euphoric"]
    vocal_style_options = ["", "Singer", "MC", "Rapper", "Spoken Word", "Chanter", "Narrator"]
    influence_tags = ["Latin Percussion", "Tribal", "Breakbeat", "Funk", "Jazz", "Afrobeat", "Dub", "Reggae", "Garage", "Techno", "Acid", "Detroit", "Chicago", "UK Bass", "Synthwave", "Ambient Pads", "Hip Hop", "Soul", "Spoken Word", "Boom Bap", "Trap Beats"]
    structure_tags = ["[Intro]", "[Verse]", "[Pre-Chorus]", "[Chorus]", "[Post-Chorus]", "[Build-Up]", "[Drop]", "[Break]", "[Breakdown]", "[Bridge]", "[Hook]", "[Solo]", "[Riff]", "[Interlude]", "[Outro]", "[Fade In]", "[Fade Out]", "[Instrumental]", "[Guitar Solo]", "[Drum Solo]", "[Piano Solo]", "[Bass Solo]", "[Big Finish]", "[Refrain]"]
    default_song_structure = ["[Intro]", "[Build-Up]", "[Drop]", "[Breakdown]", "[Drop]", "[Outro]"]
    enhancement_tags = ["[Reset Memory]", "[Clear Elements]", "[Clear All Effects]", "[Reset to Default Settings]", "[studio recording]", "[professional mastering]", "[Dolby Atmos mix]", "[high-fidelity]", "[high-definition audio]", "[wide stereo]", "[##autotune]", "[Dolby Surround]"]
    default_enhancements = ["[Reset Memory]", "[Clear Elements]", "[Clear All Effects]", "[Reset to Default Settings]", "[studio recording]", "[professional mastering]", "[Dolby Atmos mix]", "[high-fidelity]"]

    def build(self):
        return MainLayout()

if __name__ == '__main__':
    PromptBuilderApp().run()
