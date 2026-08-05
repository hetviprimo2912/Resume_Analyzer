from parser.models import ResumeChunk




def create_chunks(blocks):

    chunks = []

    chunk_id = 1

    for block in blocks:

        section = block.title.replace(" ", "").upper()

        # ----------------------------------------
        # Smart handling for PROJECTS
        # ----------------------------------------
        if section == "PROJECTS":

            current_project = None
            current_lines = []

            lines = block.lines

            for index, line in enumerate(lines):

                text = line.text.strip()

                next_line = ""

                if index + 1 < len(lines):
                    next_line = lines[index + 1].text.strip().lower()

                is_new_project = next_line.startswith("tech stack")

                if is_new_project:

                    # Save previous project
                    if current_lines:

                        content = "\n".join(current_lines)

                        chunks.append(
                            ResumeChunk(
                                chunk_id=chunk_id,
                                page=block.page,
                                section="PROJECTS",
                                subsection=current_project,
                                content=content,
                                character_count=len(content)
                            )
                        )

                        chunk_id += 1

                    # Start new project
                    current_project = text
                    current_lines = [text]

                else:

                    current_lines.append(text)

            # Save final project
            if current_lines:

                content = "\n".join(current_lines)

                chunks.append(
                    ResumeChunk(
                        chunk_id=chunk_id,
                        page=block.page,
                        section="PROJECTS",
                        subsection=current_project,
                        content=content,
                        character_count=len(content)
                    )
                )

                chunk_id += 1


        # ----------------------------------------
        # Every other section
        # ----------------------------------------
        else:

            content = "\n".join(
                line.text
                for line in block.lines
            )

            chunks.append(
                ResumeChunk(
                    chunk_id=chunk_id,
                    page=block.page,
                    section=block.title,
                    subsection=None,
                    content=content,
                    character_count=len(content)
                )
            )

            chunk_id += 1

    return chunks