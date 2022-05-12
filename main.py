from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-", '^']
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        self.solution.text = str('0')
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "^", "+"],
            ['(', ')', 'AC', 'C']
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                if label in '(':
                    button.bind(on_press=self.write_left_bracket)
                elif label == ')':
                    button.bind(on_press=self.write_right_bracket)
                else:
                    button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def write_left_bracket(self,button):
        if self.solution.text[len(self.solution.text)-1] in '123456789':
            self.solution.text = self.solution.text+'*('
        if self.solution.text[len(self.solution.text)-1] in '+-/*^':
            self.solution.text = self.solution.text()+'('

    def write_right_bracket(self,button):
        if self.solution.text.count(')') == self.solution.text.count('('):
            pass
        elif self.solution.text[len(self.solution.text)-1] in '123456789':
            self.solution.text = self.solution.text + ')'


    def on_button_press(self, number):
        if number.text == "C":
            self.solution.text = self.solution.text[0:len(self.solution.text)-1]
        elif number.text == 'AC':
            self.solution.text = ''
        elif self.solution.text == '0':
            self.solution.text = str(number.text)
        elif number.text == '-' and self.solution.text[len(self.solution.text)-1] == '(':
            self.solution.text = self.solution.text+str(number.text)
        elif str(number.text) in '.+-*/^(%' and self.solution.text[len(self.solution.text)-1] in '+-*/^(.':
            tmp_str = self.solution.text[0:len(self.solution.text)-1]
            self.solution.text = tmp_str + str(number.text)
        else:
            self.solution.text = self.solution.text+str(number.text)

    def on_solution(self, button):
        result = self.solution.text
        if '^' in result:
            result = result.replace('^', '**')
        if result[len(result)-1] in '+-/**%':
            self.solution.text = result[0:len(result)-1]
        else:
            result = str(eval(result))
            self.solution.text = result


if __name__ == "__main__":
    app = MainApp()
    app.run()