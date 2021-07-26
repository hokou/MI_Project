
const file_upload = document.querySelector("#file-upload");
let file_btn = document.querySelector("#file-btn");

file_upload.addEventListener("change", (e) => {
  console.log(e.target.files); // get file object
});


file_btn.addEventListener("click", upload);

function upload() {
    let files = file_upload.files[0];
    if (typeof (files) == "undefined" || files.size <= 0) {
        alert("請選擇檔案");
        return;
    }
    let form = new FormData();
    form.append("files", files[0]);
    fetch('/api/data/upload', {
    method: 'POST',
    body: form,
    })
}