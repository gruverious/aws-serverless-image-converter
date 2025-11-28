const UPLOAD_LAMBDA_URL = "Your_UPLOAD_LAMBDA_URL";
const LIST_LAMBDA_URL   = "YOUR_LIST_LAMBDA_URL";

// File upload via presigned URL
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!fileInput.files.length) {
    status.innerText = "Please select a file first.";
    return;
  }

  const file = fileInput.files[0];

  try {
    status.innerText = "Requesting upload URL...";

    // Extracting presigned URL from Lambda 
    const res = await fetch(UPLOAD_LAMBDA_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fileName: file.name,
        contentType: file.type || "image/jpeg"
      })
    });

    if (!res.ok) {
      status.innerText = "Failed to get upload URL.";
      return;
    }

    const data = await res.json();
    const uploadUrl = data.uploadUrl;

    status.innerText = "Uploading to S3...";

    // image uploaded directly to s3
    const uploadRes = await fetch(uploadUrl, {
      method: "PUT",
      body: file
    });

    if (!uploadRes.ok) {
      status.innerText = "S3 upload failed.";
      return;
    }

    status.innerText = "Uploaded! PNG will appear in the output bucket shortly.";
    fileInput.value = "";

    // Auto refreshes file list
    setTimeout(loadFiles, 3000);

  } catch (err) {
    console.error(err);
    status.innerText = "Error occurred. Check console.";
  }
}

// load output files 
async function loadFiles() {
  const listEl = document.getElementById("fileList");
  listEl.innerHTML = "<li>Loading files...</li>";

  try {
    const res = await fetch(LIST_LAMBDA_URL);

    if (!res.ok) {
      listEl.innerHTML = "<li>Failed to load files.</li>";
      return;
    }

    const data = await res.json();
    const files = data.files || [];

    if (files.length === 0) {
      listEl.innerHTML = "<li>No converted files yet.</li>";
      return;
    }

    listEl.innerHTML = "";

    files.forEach(file => {
      const li = document.createElement("li");

      const link = document.createElement("a");
      link.href = file.downloadUrl;
      link.textContent = `${file.fileName} (${(file.size / 1024).toFixed(2)} KB)`;
      link.target = "_blank";

      const delBtn = document.createElement("button");
      delBtn.textContent = "Delete";
      delBtn.style.marginLeft = "10px";

      delBtn.onclick = async () => {
        const confirmed = confirm("Delete this file?");
        if (!confirmed) return;

        await fetch(LIST_LAMBDA_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            fileName: file.fileName
          })
        });

        loadFiles(); 
        // refresh after delete
      };

      li.appendChild(link);
      li.appendChild(delBtn);
      listEl.appendChild(li);
    });

  } catch (err) {
    console.error(err);
    listEl.innerHTML = "<li>Error loading files.</li>";
  }
}


// Auto load files when page opens
window.onload = loadFiles;
