from services.resume_indexer import index_resume


def main():

    resume_id = index_resume(
        "uploads/sample_resume.pdf"
    )

    print()

    print("Resume Indexed Successfully")

    print(f"Resume ID : {resume_id}")


if __name__ == "__main__":
    main()