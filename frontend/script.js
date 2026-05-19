async function analyzeResumes() {

    // Get Job Description
    const jobDescription =
        document.getElementById("jobDescription").value;

    // Create FormData
    const formData = new FormData();

    // Add Job Description
    formData.append(
        "job_description",
        jobDescription
    );

    // Add Resume Files
    formData.append(
        "resume1",
        document.getElementById("resume1").files[0]
    );

    formData.append(
        "resume2",
        document.getElementById("resume2").files[0]
    );

    formData.append(
        "resume3",
        document.getElementById("resume3").files[0]
    );

    formData.append(
        "resume4",
        document.getElementById("resume4").files[0]
    );

    try {

        // Send Request to Backend
        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        // Convert Response to JSON
        const data = await response.json();

        console.log(data);

        // Get Results Div
        const resultDiv =
            document.getElementById("results");

        // Clear Previous Results
        resultDiv.innerHTML = "";

        // Add Heading
        resultDiv.innerHTML = `
            <h2>Resume Rankings</h2>
        `;

        // Loop Through Rankings
        data.rankings.forEach((item, index) => {

            resultDiv.innerHTML += `

                <div class="result-card">

                    <h3>
                        Rank ${index + 1}
                    </h3>

                    <p>
                        <strong>Resume:</strong>
                        ${item.resume}
                    </p>

                    <p>
                        <strong>Match Score:</strong>
                        ${item.match_score}%
                    </p>

                    <p>
                        <strong>Matched Skills:</strong>
                        ${item.matched_skills.join(", ")}
                    </p>

                    <p>
                        <strong>Reason:</strong>
                        ${item.shortlisted_reason}
                    </p>

                </div>

            `;

        });

        alert("Resume Analysis Completed!");

    }

    catch (error) {

        console.log(error);

        alert("Error Connecting Backend");

    }

}