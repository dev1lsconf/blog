#!/usr/bin/env python
import os
import subprocess
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Input, TextArea, Button, Static

class MarkdownPostCreator(App):
    """A TUI application to create markdown posts with consistent front matter."""

    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("ctrl+s", "save_post", "Save Post"),
        ("ctrl+p", "publish_to_github", "Publish to GitHub"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-grid"):
            with Container(id="metadata-container"):
                yield Static("Post Metadata", classes="section-title")
                yield Input(placeholder="Post Title", id="title", classes="metadata-input")
                yield Input(placeholder="Publish Date (YYYY-MM-DD)", id="publish_date", classes="metadata-input")
                yield Input(placeholder="Post Summary", id="summary", classes="metadata-input")
            
            with VerticalScroll(id="content-container"):
                yield Static("Post Content", classes="section-title")
                yield TextArea(id="content", language="markdown", classes="content-editor")
            
            with Container(id="buttons-container"):
                yield Button("Save Post", id="save", variant="primary")
                yield Button("Publish to GitHub", id="publish", variant="success")
                yield Button("Quit", id="quit", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Set default values when the app mounts."""
        self.query_one("#publish_date", Input).value = datetime.now().strftime("%Y-%m-%d")
        self.query_one("#content", TextArea).focus()

    def action_save_post(self) -> None:
        """Action to save the post."""
        self.save_post()

    def action_publish_to_github(self) -> None:
        """Action to publish the post to GitHub."""
        self.publish_to_github()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.save_post()
        elif event.button.id == "publish":
            self.publish_to_github()
        elif event.button.id == "quit":
            self.exit()

    def save_post(self) -> Path:
        """Save the post to a markdown file in the blog directory."""
        title = self.query_one("#title", Input).value.strip()
        publish_date = self.query_one("#publish_date", Input).value.strip()
        summary = self.query_one("#summary", Input).value.strip()
        content = self.query_one("#content", TextArea).text.strip()

        if not title:
            self.notify("Title is required!", severity="error")
            return None

        try:
            datetime.strptime(publish_date, "%Y-%m-%d")
        except ValueError:
            self.notify("Invalid date format! Use YYYY-MM-DD", severity="error")
            return None

        front_matter = f"""---
title: {title}
publish_date: {publish_date}
summary: {summary}
---

{content}
"""

        blog_dir = Path("posts")
        blog_dir.mkdir(exist_ok=True)

        filename = blog_dir / f"{title.lower().replace(' ', '-')}.md"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(front_matter)
            self.notify(f"Post saved as {filename}!", severity="success")
            return filename
        except IOError as e:
            self.notify(f"Error saving file: {e}", severity="error")
            return None

    def publish_to_github(self) -> None:
        """Publish the post to GitHub by executing git commands."""
        filename = self.save_post()
        if not filename:
            return

        try:
            subprocess.run(["git", "add", str(filename)], check=True)
            commit_message = f"Add new post: {filename.name}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)
            self.notify("Post successfully published to GitHub!", severity="success")
        except subprocess.CalledProcessError as e:
            self.notify(f"Git operation failed: {e}", severity="error")
        except Exception as e:
            self.notify(f"Error publishing to GitHub: {e}", severity="error")

if __name__ == "__main__":
    app = MarkdownPostCreator()
    app.run()
