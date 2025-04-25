#!/usr/bin/env python
import os
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, TextArea, Button

class MarkdownPostCreator(App):
    """A TUI application to create markdown posts with consistent front matter."""

    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("ctrl+s", "save_post", "Save Post"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(placeholder="Post Title", id="title"),
            Input(placeholder="Publish Date (YYYY-MM-DD)", id="publish_date"),
            Input(placeholder="Post Summary", id="summary"),
            TextArea(id="content", language="markdown"),
        )
        yield Container(
            Button("Save Post", id="save"),
            Button("Quit", id="quit"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set default values when the app mounts."""
        self.query_one("#publish_date", Input).value = datetime.now().strftime("%Y-%m-%d")
        self.query_one("#content", TextArea).focus()

    def action_save_post(self) -> None:
        """Action to save the post."""
        self.save_post()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.save_post()
        elif event.button.id == "quit":
            self.exit()

    def save_post(self) -> None:
        """Save the post to a markdown file in the blog directory."""
        title = self.query_one("#title", Input).value.strip()
        publish_date = self.query_one("#publish_date", Input).value.strip()
        summary = self.query_one("#summary", Input).value.strip()
        content = self.query_one("#content", TextArea).text.strip()

        if not title:
            self.notify("Title is required!", severity="error")
            return

        try:
            # Validate date format
            datetime.strptime(publish_date, "%Y-%m-%d")
        except ValueError:
            self.notify("Invalid date format! Use YYYY-MM-DD", severity="error")
            return

        # Create front matter with exact formatting
        front_matter = f"""---
title: {title}
publish_date: {publish_date}
summary: {summary}
---

{content}
"""

        # Create blog directory if it doesn't exist
        blog_dir = Path("posts")
        blog_dir.mkdir(exist_ok=True)

        # Create filename from title
        filename = blog_dir / f"{title.lower().replace(' ', '-')}.md"
        
        # Save to file
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(front_matter)
            self.notify(f"Post saved as {filename}!", severity="success")
        except IOError as e:
            self.notify(f"Error saving file: {e}", severity="error")

if __name__ == "__main__":
    app = MarkdownPostCreator()
    app.run()
