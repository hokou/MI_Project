
const file_upload = document.querySelector("#file-upload");
let file_btn = document.querySelector("#file-btn");

load_data();

file_upload.addEventListener("change", (e) => {
  console.log(e.target.files); // get file object
});

file_btn.addEventListener("click", upload);

function upload() {
    let files = file_upload.files;
    if (typeof (files) == "undefined" || files.size <= 0) {
        alert("請選擇檔案");
        return;
    }
    let form = new FormData();

    for (let file of files) {
      // form.append("files[]",file, file.name);
      form.append("files",file, file.name);
    }
    console.log(form);
    fetch('/api/data/upload', {
    method: 'POST',
    body: form,
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
          alert("上傳 OK");
          load_data();
        } else if (data.error) {
            console.log(data);
            alert(data.message);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

function load_data() {
    fetch('/api/data/load', {
        method: 'GET',
        }).then((res) => res.json())
        .then((data) => {
            if (data.id) {
                console.log(data);
                addblock(data.data);
            } else if (data.error) {
                console.log(data);
            }
        })
        .catch((error) => {
            console.log("err:", error)
        });
}


function addblock(data){
    let main = document.getElementById("main-block");
    while (main.firstChild) {
        main.removeChild(main.firstChild);
    };
    for (let i=0;i<data.length;i++) {
        let div = document.createElement("div");
        let imgdiv = document.createElement("div");
        let img = document.createElement("img");
        let p1 = document.createElement("p");
        let p2 = document.createElement("p");
        let p3 = document.createElement("p");
        let input = document.createElement("input");

        main.appendChild(div);
        div.appendChild(imgdiv);
        imgdiv.appendChild(img);
        div.appendChild(p1);
        div.appendChild(p2);
        div.appendChild(p3);
        div.appendChild(input);

        div.className = "sub-block";
        imgdiv.className = "img-block";
        img.src = data[i]["img"];
        p1.textContent = data[i]["file_name"];
        p2.textContent = `patient ID：${data[i]["patient_ID"]}`;
        p3.textContent = `patient Name：${data[i]["patient_name"]}`;
        input.type="radio";
        input.name="userchoice";
        input.value= `${i}`;
    }
}