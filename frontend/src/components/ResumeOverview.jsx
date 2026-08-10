function ResumeOverview() {
  return (
    <section className="resume-overview">
      <div className="section-heading">
        <div>
          <h3>Resume Overview</h3>
          <p>Quick insights from your uploaded resume</p>
        </div>
      </div>

      <div className="overview-grid">
        {/* Summary */}
        <div className="overview-card summary-card">
          <div className="card-icon">✦</div>

          <div className="card-label">Resume Summary</div>

          <h4>Resume analyzed successfully</h4>

          <p>
            Your resume is indexed and ready. Ask questions about your
            experience, skills, projects, education, and more.
          </p>
        </div>

        {/* ATS */}
        <div className="overview-card ats-card">
          <div className="card-icon">◈</div>

          <div className="card-label">ATS Readiness</div>

          <div className="ats-placeholder">--</div>

          <p className="ats-text">
            Add a job description to calculate your ATS score and job match.
          </p>

          <button className="secondary-action">
            + Add Job Description
          </button>
        </div>

        {/* Improvements */}
        <div className="overview-card improvement-card">
          <div className="card-icon">↗</div>

          <div className="card-label">Key Improvement Areas</div>

          <ul className="improvement-list">
            <li>
              <span>01</span>
              Quantify project achievements
            </li>

            <li>
              <span>02</span>
              Highlight measurable impact
            </li>

            <li>
              <span>03</span>
              Add relevant keywords for target roles
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}

export default ResumeOverview;