        // Show generated text box and generate cover letter
        document.getElementById("generate-btn").addEventListener("click", function (event) {
            event.preventDefault();

            const jobDescription = document.getElementById("job-description").value;
            const companyName = document.getElementById("company-name").value;
            const yourName = document.getElementById("your-name").value;

            // // Check if job description, company name, and your name are entered
            // if (jobDescription === "" || companyName === "" || yourName === "") {
            //     alert("Please enter all fields.");
            //     return;
            // }

            // Generate cover letter based on job description, company name, and your name
            const coverLetter = `Dear Hiring Manager,\n\nI am writing to express my interest in the ${jobDescription} position at ${companyName}. As a ${yourName}, I believe I would be an excellent candidate for this role.\n\nThank you for considering my application. I look forward to hearing from you soon.\n\nSincerely,\nYour Name`;

            // Show generated cover letter card
            const card = document.createElement("div");
            card.classList.add("card", "my-3", "w-50", "mx-auto");
            const cardBody = document.createElement("div");
            cardBody.classList.add("card-body", "text-center");
            card.appendChild(cardBody);
            const cardTitle = document.createElement("h5");
            cardTitle.classList.add("card-title", "fw-bold", "mb-4");
            cardTitle.textContent = "Generated Cover Letter";
            cardBody.appendChild(cardTitle);
            const cardText = document.createElement("p");
            cardText.classList.add("card-text");
            cardText.style.fontSize = "16px";

            cardText.classList.add("card-text");
            cardBody.appendChild(cardText);
            document.getElementById("generated-letter-card").style.display = "block";
            document.getElementById("generated-letter").textContent = "";
            document.getElementById("generated-letter").appendChild(card);

            // Render cover letter text one letter at a time
            let i = 0;
            const timer = setInterval(function () {
                if (i < coverLetter.length) {
                    cardText.textContent += coverLetter.charAt(i);
                    i++;
                } else {
                    clearInterval(timer);
                }
            }, 20);
        });

        const copyBtn = document.getElementById('copy-btn');
        const generatedLetter = document.getElementById('generated-letter');
      
        copyBtn.addEventListener('click', () => {
          // Create a temporary textarea to hold the text
          const tempTextarea = document.createElement('textarea');
          tempTextarea.value = generatedLetter.innerText;
      
          // Add the textarea to the document
          document.body.appendChild(tempTextarea);
      
          // Copy the text to the clipboard
          tempTextarea.select();
          document.execCommand('copy');
      
          // Remove the textarea from the document
          document.body.removeChild(tempTextarea);
      
          // Display a success message
          alert('Copied to clipboard!');
        });
