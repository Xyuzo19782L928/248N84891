import os
import re

class CampaignManager:
    def __init__(self, data_dir="../data"):
        """
        Initialize the campaign manager with the data directory.
        """
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created data directory: {self.data_dir}")

    def create_markdown_file(self, sub_path, content):
        """
        Create a new Markdown file with the given content.
        """
        file_path = os.path.join(self.data_dir, sub_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"File created: {file_path}")

    def update_markdown_section(self, sub_path, section_name, new_content):
        """
        Update a specific section in a Markdown file or append it if it doesn't exist.
        """
        file_path = os.path.join(self.data_dir, sub_path)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Creating a new file.")
            self.create_markdown_file(sub_path, f"# {section_name}\n\n{new_content}")
            return

        with open(file_path, "r") as file:
            content = file.read()

        # Regex to find and replace the targeted section
        pattern = rf"(## {section_name}.*?)(##|\Z)"
        if re.search(pattern, content, flags=re.DOTALL):
            updated_content = re.sub(
                pattern,
                rf"## {section_name}\n\n{new_content}\n\n\2",
                content,
                flags=re.DOTALL
            )
        else:
            # Append the section if it doesn't exist
            updated_content = content + f"\n\n## {section_name}\n\n{new_content}\n"

        with open(file_path, "w") as file:
            file.write(updated_content)
        print(f"Section '{section_name}' updated in {file_path}")

    def combine_markdown_files(self, output_path, *sub_paths):
        """
        Combine multiple Markdown files into one.
        """
        output_file = os.path.join(self.data_dir, output_path)
        with open(output_file, "w") as outfile:
            for sub_path in sub_paths:
                file_path = os.path.join(self.data_dir, sub_path)
                if os.path.exists(file_path):
                    with open(file_path, "r") as infile:
                        outfile.write(f"# {os.path.basename(file_path)}\n\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n---\n\n")
                else:
                    print(f"File {file_path} not found.")
        print(f"Combined file created: {output_file}")


# Example Usage
if __name__ == "__main__":
    # Initialize the campaign manager
    manager = CampaignManager(data_dir="../data")

    # Create a new character file
    napy_content = """# Napy

## Basic Information
- **Race**: Human
- **Class**: Rogue
- **Background**: Urban Explorer
- **Alignment**: Neutral Good
- **Level**: 3

## Stats
| Ability        | Score | Modifier |
|----------------|-------|----------|
| Strength       | 10    | +0       |
| Dexterity      | 16    | +3       |
| Constitution   | 14    | +2       |
| Intelligence   | 12    | +1       |
| Wisdom         | 10    | +0       |
| Charisma       | 14    | +2       |

## Inventory
- Rusty Dagger (Magical)
- 15 Gold Coins
"""
    manager.create_markdown_file("characters/napy.md", napy_content)

    # Update the inventory section in Napy's file
    manager.update_markdown_section("characters/napy.md", "Inventory", "- Rusty Dagger (Magical)\n- 20 Gold Coins")

    # Combine notes into one file
    manager.combine_markdown_files(
        "combined_campaign.md",
        "characters/napy.md",
        "journal/session_1.md"
    )
