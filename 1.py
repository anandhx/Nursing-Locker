import csv

# Define the input file
input_file = 'input.csv'

# Initialize the HTML structure
html_output = """
<section id="study-notes" class="study-notes section">
  <div class="container" data-aos="fade-up">
    <h2 class="section-title text-center mb-4">Study Notes</h2>
    <p class="text-center mb-5">Select your year to access study notes for specific subjects.</p>

    <!-- Year Selector -->
    <div class="d-flex justify-content-center mb-4">
"""

# Define year buttons
years = ["First Year", "Second Year", "Third Year", "Fourth Year"]
for year in years:
    year_id = year.lower().replace(" ", "-")
    html_output += f'      <button class="btn btn-outline-primary mx-2 year-button" onclick="showSubjects(\'{year_id}\')">{year}</button>\n'

html_output += "    </div>\n\n"

# Initialize data structure for notes
notes_data = {}

# Read data from CSV
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        main_folder = row['Main Folder']
        sub_folder = row['Sub Folder']
        file_name = row['File Name']
        shareable_link = row['Sharable Link']
        
        # Convert the Google Drive shareable link to a direct download link
        file_id = shareable_link.split('/')[5]
        download_link = f"https://drive.google.com/uc?export=download&id={file_id}"

        if main_folder not in notes_data:
            notes_data[main_folder] = {}
        if sub_folder not in notes_data[main_folder]:
            notes_data[main_folder][sub_folder] = []
        notes_data[main_folder][sub_folder].append({'name': file_name, 'link': download_link})

# Generate HTML for each year
for year, subjects in notes_data.items():
    year_id = year.lower().replace(" ", "-")
    html_output += f'    <!-- {year} Subjects -->\n'
    html_output += f'    <div id="{year_id}" class="row gy-4 subject-section d-none">\n'

    for subject, files in subjects.items():
        subject_id = f"{subject.lower().replace(' ', '-')}-sub-notes"
        html_output += f'      <div class="col-xl-3 col-md-6 d-flex">\n'
        html_output += f'        <div class="service-item position-relative">\n'
        html_output += f'          <div class="icon"><i class="bi bi-book"></i></div>\n'
        html_output += f'          <h4>\n'
        html_output += f'            <a href="#" class="stretched-link" onclick="showSubNotes(\'{subject_id}\')">{subject}</a>\n'
        html_output += f'          </h4>\n'
        html_output += f'          <p>Notes for {subject}.</p>\n'
        html_output += f'        </div>\n'
        html_output += f'      </div>\n'

    html_output += f'    </div>\n\n'

# Add sub-notes JavaScript and toast functionality
html_output += """
    <!-- Sub-Notes Section -->
    <div id="sub-notes-container" class="mt-5">
      <h4 class="text-center" id="sub-notes-title"></h4>
      <ul id="sub-notes-list" class="list-unstyled text-center mt-3"></ul>
    </div>

    <!-- Toast Notification -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div id="downloadToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto">Download</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          File is downloading...
        </div>
      </div>
    </div>

  </div>
</section>

<script>
  const subNotesData = {
"""

# Add JavaScript for sub-notes
for year, subjects in notes_data.items():
    for subject, files in subjects.items():
        subject_id = f"{subject.lower().replace(' ', '-')}-sub-notes"
        html_output += f"    '{subject_id}': {{\n"
        html_output += f"      title: '{subject} - Sub Notes',\n"
        html_output += f"      notes: [\n"
        for file in files:
            html_output += f"        {{ name: '{file['name']}', link: '{file['link']}' }},\n"
        html_output += f"      ],\n"
        html_output += f"    }},\n"

html_output += """
  };

  function showSubjects(year) {
    document.querySelectorAll('.subject-section').forEach(section => {
      section.classList.add('d-none');
    });
    document.getElementById(year).classList.remove('d-none');
    clearSubNotes();
  }

  function showSubNotes(subjectId) {
    const subNotes = subNotesData[subjectId];
    if (subNotes) {
      document.getElementById('sub-notes-title').textContent = subNotes.title;
      const subNotesList = document.getElementById('sub-notes-list');
      subNotesList.innerHTML = '';
      subNotes.notes.forEach(note => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${note.name}
          <a href="${note.link}" download class="btn btn-sm btn-success mx-1" onclick="showToast()">
            <i class="bi bi-download"></i> Download
          </a>
        `;
        subNotesList.appendChild(li);
      });
    }
  }

  function clearSubNotes() {
    document.getElementById('sub-notes-title').textContent = '';
    document.getElementById('sub-notes-list').innerHTML = '';
  }

  function showToast() {
    const toastElement = document.getElementById('downloadToast');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
  }
</script>
"""

# Save the HTML output to a file
with open('study_notes.html', 'w') as output_file:
    output_file.write(html_output)

print("HTML file generated: study_notes.html")
