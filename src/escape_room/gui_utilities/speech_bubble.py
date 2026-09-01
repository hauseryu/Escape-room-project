
class SpeechBubble:

    def __init__(self,bubbles,choices=None,evaluate_choices_callback=None):
        self.current_bubble = None
        self.bubbles = bubbles
        self.choices = choices
        self.evaluate_choices_callback = evaluate_choices_callback

    def show_bubble(self, canvas):

            self.current_bubble = 0
            self.draw_bubble(canvas)

            # keyboard navigation
            canvas.focus_set()
            if len(self.bubbles) > 1:
                canvas.bind("<Left>", self.previous_bubble)
                canvas.bind("<Right>", self.next_bubble)
            canvas.bind("<Escape>", lambda e: self.close_bubble(canvas))

    def draw_bubble(self, canvas):
        # remove old bubble
        canvas.delete("bubble")

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # dark overlay
        canvas.create_rectangle(
            0,
            0,
            w,
            h,
            fill="black",
            stipple="gray50",
            tags="bubble"
        )

        # pergament
        margin_x = w * 0.2

        top = h * 0.15 + 100
        bottom = h - 50

        canvas.create_rectangle(
            margin_x,
            top,
            w - margin_x,
            bottom,
            fill="#d8c3a5",
            outline="#7a5230",
            width=4,
            tags="bubble bubble_content"
        )
        
        arrow_space = 130

        text_x = margin_x + arrow_space
        text_y = top + 100

        text_width = w - 2 * margin_x - 2 * arrow_space

        # current bubble text
        canvas.create_text(
            text_x,
            text_y,
            text=self.bubbles[self.current_bubble],
            width=text_width,
            font=("Times New Roman", 27),
            justify="left",
            anchor="nw",
            fill="#3b281b",
            tags="bubble bubble_content"
        )
        
        arrow_offset = 70

        # left arrow
        if self.current_bubble > 0 and len(self.bubbles)>1:
            canvas.create_text(
                margin_x + arrow_offset,
                h / 2,
                text="←",
                font=("Arial", 35, "bold"),
                fill="#5c3b20",
                tags="bubble previous"
            )

        # right arrow
        if (self.current_bubble < len(self.bubbles) - 1) and len(self.bubbles)>1:
            canvas.create_text(
                w - margin_x - arrow_offset,
                h / 2,
                text="→",
                font=("Arial", 35, "bold"),
                fill="#5c3b20",
                tags="bubble next"
            )

        # Display "1 / 3"
        if len(self.bubbles)>1:
            canvas.create_text(
                w / 2,
                bottom - 35,
                text=f"{self.current_bubble + 1} / {len(self.bubbles)}",
                font=("Times New Roman", 18),
                fill="#3b281b",
                tags="bubble bubble_content"
            )

        # Close
        canvas.create_text(
            w - margin_x - 30,
            top + 30,
            text="✕",
            font=("Arial", 20, "bold"),
            fill="#5c3b20",
            tags="bubble bubble_close"
        )

        # Choices
        if self.choices != None:
            offset_choices = len(self.choices) * 50
            for index, choice in enumerate(self.choices):
                tag = "choice" + str(index)
                canvas.create_text(
                    text_x + 20,
                    bottom - 60 - offset_choices + index * 50,
                    text=choice[0], # get choice text
                    anchor="nw",  # draw arranged to left based on x point
                    justify="left",
                    width=text_width,
                    font=("Times New Roman", 30),
                    fill="#6825b6",
                    tags=(tag,"bubble")
                )   
                canvas.tag_bind(
                    tag,
                    "<Button-1>",
                    lambda e, t=tag: self.bubble_choice(e, canvas, t)
                )
                #  mouse enters text => change to hand symbol
                canvas.tag_bind(
                    tag,
                    "<Enter>",
                    lambda e: canvas.config(cursor="hand2")
                )
                # mouse leaves text => change pointer back to normal
                canvas.tag_bind(
                    tag,
                    "<Leave>",
                    lambda e: canvas.config(cursor="")
                )            

        # Click on X
        canvas.tag_bind(
            "bubble_close",
            "<Button-1>",
            lambda e: self.close_bubble(canvas)
        )

        if len(self.bubbles)>1:
            # Click on left arrow
            canvas.tag_bind(
                "previous",
                "<Button-1>",
                lambda e: self.previous_bubble(e, canvas)
            )

            # Click on right arrow
            canvas.tag_bind(
                "next",
                "<Button-1>",
                lambda e: self.next_bubble(e, canvas)
            )

            # Click on left/right side of the parchment
            canvas.tag_bind(
                "bubble_content",
                "<Button-1>",
                lambda e: self.click_bubble(e, canvas)
            )

    def next_bubble(self, event, canvas=None):
        if canvas is None:
            canvas = event.widget

        if self.current_bubble < len(self.bubbles) - 1:
            self.current_bubble += 1
            self.draw_bubble(canvas)

    def previous_bubble(self, event, canvas=None):
        if canvas is None:
            canvas = event.widget

        if self.current_bubble > 0:
            self.current_bubble -= 1
            self.draw_bubble(canvas)

    def click_bubble(self, event, canvas):
        """Click on the left/right side of the bubble."""
        w = canvas.winfo_width()

        if event.x < w / 2:
            self.previous_bubble(event, canvas)
        else:
            self.next_bubble(event, canvas)

    def bubble_choice(self, event, canvas, tag):
        print("[DEBUG] choice selected:",tag)
        choice=int(tag[6:]) # get choice number
        self.close_bubble(canvas) # after selection close the bubble
        self.evaluate_choices_callback(self.choices,choice) # call callback to further evaluate the choice action sequence

    def close_bubble(self, canvas):
        canvas.delete("bubble")

        canvas.unbind("<Left>")
        canvas.unbind("<Right>")
        canvas.unbind("<Escape>")