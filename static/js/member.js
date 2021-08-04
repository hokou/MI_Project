
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
        let imga = document.createElement("a");
        let img = document.createElement("img");
        let p1 = document.createElement("p");
        let p2 = document.createElement("p");
        let p3 = document.createElement("p");
        let close = addclose(data[i]["file_id"]);

        main.appendChild(div);
        div.appendChild(imgdiv);
        imgdiv.appendChild(imga);
        imga.appendChild(img);
        div.appendChild(p1);
        div.appendChild(p2);
        div.appendChild(p3);
        div.appendChild(close);

        // div.className = "sub-block";
        div.classList.add("sub-block", "m-1");
        imgdiv.className = "img-block";
        imga.href = `/api/data/file/${data[i]["file_id"]}`;
        img.src = data[i]["img"];
        p1.textContent = data[i]["file_name"];
        p2.textContent = `patient ID：${data[i]["patient_ID"]}`;
        p3.textContent = `patient Name：${data[i]["patient_name"]}`;
    }
    let close_btn = document.querySelectorAll(".close");
    close_addevent(close_btn);
}

function addclose(data){
    let div = document.createElement("div");
    let img = document.createElement("img");
    let input = document.createElement("input");
    div.appendChild(img);
    div.appendChild(input);
    div.className = "close";
    img.className = "close-img";
    input.type = "hidden";
    input.value = data;
    return div
}

function close_addevent(close) {
    for (let i = 0; i < close.length; i++) {
        close[i].addEventListener("click", e=> {
            let close_select = e.target.querySelector('input').value;
            console.log(close_select);
            close_file(close_select);
        });
    }
}

function close_file(select) {
    let yes = confirm('是否刪除檔案？');
    if (yes) {
        alert('確定');
    } else {
        alert('取消');
    }
}