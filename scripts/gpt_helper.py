# Re-attempt the process with proper debugging
import os


def split_dnd_log(input_file, output_dir, max_chunk_size=10000):
    """
    Splits a large text file into smaller chunks, ensuring that splits occur only at the end of user inputs.
    Arguments:
    - input_file: Path to the large input text file.
    - output_dir: Directory where the split files will be saved.
    - max_chunk_size: Maximum number of characters per chunk.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Try reading the file with UTF-8 encoding, fallback to a broader encoding if it fails
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Trying latin-1 encoding.")
        with open(input_file, 'r', encoding='latin-1') as file:
            content = file.read()

    # Identify split points where lines start with "User:" (logical split points)
    lines = content.splitlines()
    chunks = []
    current_chunk = []
    current_size = 0

    for line in lines:
        # Add the line to the current chunk
        current_chunk.append(line)
        current_size += len(line) + 1  # Account for the newline character

        # If the chunk size exceeds the limit and the line starts with "User:", split
        if current_size >= max_chunk_size and (line.startswith("User:") or line.startswith("Du:")):
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_size = 0

    # Add remaining content as the final chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    # Write each chunk to a file
    output_files = []
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f"dnd_log_chunk_{i + 1}.txt")
        with open(output_path, "w", encoding='utf-8') as output_file:
            output_file.write(chunk)
        output_files.append(output_path)

    return output_files

if __name__ == "__main__":

    # File paths
    input_path = "../data/input/DnD_Log.txt"
    output_directory = "../data/input/junked_log"

    # Run the function
    split_files = split_dnd_log(input_path, output_directory)
    split_files  # Output the list of created chunk files

