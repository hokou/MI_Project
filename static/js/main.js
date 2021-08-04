
let image_main = document.querySelector("#image-main");

let palette = document.querySelector("#palette");
let linecolor = document.querySelector("#linecolor");
let rect = document.querySelector('#rect');

let ww = document.querySelector("#ww");
let wl = document.querySelector("#wl");
let inverse = document.querySelector('#image-inverse');
let img_form = document.querySelector('#img-form');
let label_data = document.querySelector('#label-data');
let label_save_btn = document.querySelector('#label_save_btn');
let label_hid = document.querySelector('#label-hid');

const canvas = new fabric.Canvas('image-main', {
    width: 512,
    height: 512
});

let canvas_state = canvas.toJSON()


mi_fetch();
fabric_setting();
label_fetch();

function mi_fetch() {
    let url = "/api/mi/data";
    fetch(url).then(response => response.json())
        .then((result)=>{
            label_hid.value = result.fileid;
            image_data(result);
            // fabric_setting();
        }).catch(error => console.log("err:", error));
}

function image_data(result) {
    let img = result.image;
    image_render(img);
    ww.setAttribute("value",result.WW);
    wl.setAttribute("value",result.WL);
}

function fabric_setting() {
    fabric.Object.prototype.customiseCornerIcons({
        tr: { //
            icon:"/images/close_white_24dp.svg"
            ,setting: {
                cornerPadding: 10
            },
        },
    }, function() {
        canvas.renderAll();
    });

    fabric.Canvas.prototype.customiseControls({
        tr: { //右上
            action: 'remove', //刪除
            cursor: 'pointer'
        },
    }, function() {
        canvas.renderAll();
    });
}

function image_render(img) {
    fabric.Image.fromURL(img, (img) => {
        img.set({
            scaleX: canvas.width / img.width,
            scaleY: canvas.height / img.height,
            // scaleX: 1,
            // scaleY: 1,
        });
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        canvas.renderAll();
    });
}

function add_rect(canvas, width=40, height=40, left=50, top=50) {
    const rect = new fabric.Rect({
        width: width,
        height: height,
        left: left,
        top: top,
        fill: 'transparent', // 不要填滿
        stroke: linecolor.value, // 邊框顏色
        strokeWidth: 1.5
    })
        rect.setControlsVisibility({ 
        mtr: false, //禁止旋轉
    });
    canvas.add(rect);
    canvas.renderAll();
}

function midata_renew() {
    let url = "/api/mi/renew";
    let midata = {
        "ww": ww.value,
        "wl": wl.value,
        "inverse": inverse.value
    };
    console.log(midata);

    fetch(url,{
        method:'POST',
        body:JSON.stringify(midata),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            console.log(data);
            // inverse.value = data["inverse"];
            image_render(data["image"]);
        } else if (data.error) {
            console.log(data);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });

}


function inverse_change() {
    if (inverse.value === "1") {
        inverse.value = "0";
    } else if (inverse.value === "0") {
        inverse.value = "1";
    }
    console.log(inverse.value);
}


ww.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        // this.form.submit();
        inverse.value = "0";
        midata_renew();
        inverse.value = "1";
    }
}
);


wl.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        // this.form.submit();
        inverse.value = "0";
        midata_renew();
        inverse.value = "1";
        }
    }
);


inverse.addEventListener("click",function(event){
    event.preventDefault();
    midata_renew();
    inverse_change();
    // this.form.submit();
    // inverse_change();
})


linecolor.addEventListener('change',function(){
    console.log(linecolor.value);
})


rect.addEventListener('click',function(){
    add_rect(canvas);
    label_renew();
})


canvas.on('object:modified', (e) => {
    // console.log(e.target);
    canvas_state = canvas.toJSON();
    let label_list = label_coordinate(canvas_state);
    label_renew(label_list);
});

canvas.on('mouse:down', (e) => {
    // console.log(e.target);
    canvas_state = canvas.toJSON();
    let label_list = label_coordinate(canvas_state);
    label_renew(label_list);
});

function label_renew(label_list) {
    while (label_data.firstChild) {
        label_data.removeChild(label_data.firstChild);
    };

    for (let i=0;i<label_list.length;i++) {
        let p = document.createElement("p");
        label_data.appendChild(p);
        // p.textContent = label_list[i].toString();
        // p.textContent = label_list[i].join(", ");
        let new_label = text_pad(label_list[i], len=4)
        p.textContent = new_label.join(", ");
        // console.log(label_list[i]);
    }
}

function label_coordinate (canvas_data) {
    let data = canvas_data.objects;
    let label_list = [];
    for (i = 0;i<data.length;i++){
        label_list.push(coordinate_conversion(data[i]));
    }
    return label_list
}

function coordinate_conversion(data) {
    let top = Math.round(data.top);
    let left = Math.round(data.left);
    let height = Math.round(data.height * data.scaleY);
    let width = Math.round(data.width * data.scaleX);
    let label = [top, left, height, width];
    return label
}

function text_pad(str_data, len=4) {
    let new_label = [];
    for (let text of str_data) {
        text = `${text}`;
        new_label.push(text.padStart(len, '0'));
    }
    return new_label
}

function label_fetch() {
    let url = "/api/mi/label";
    fetch(url).then(response => response.json())
        .then((data) => {
        if (data.data != null) {
            console.log(data.data);
            label_hid.value = data.data.fileid;
            let label_list = data.data.label;
            label_renew(label_list);
            canvas_label_renew(label_list);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

label_save_btn.addEventListener('click', label_save)

function label_save() {
    canvas_state = canvas.toJSON();
    let label_list = label_coordinate(canvas_state);
    let label_data = {
        "fileid":Number(label_hid.value),
        "num":label_list.length,
        "label":label_list
    };
    // console.log(label_data);
    label_save_fetch(label_data);
}

function label_save_fetch(label_data) {
    let url = "/api/mi/labelsave";
    fetch(url,{
        method:'POST',
        body:JSON.stringify(label_data),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            console.log(data);
            alert("儲存 OK");
        } else if (data.error) {
            console.log(data);
            alert(data.message);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

function canvas_label_renew(label_list) {
    for(i=0;i<label_list.length;i++){
        let top = label_list[i][0];
        let left = label_list[i][1];
        let height = label_list[i][2];
        let width = label_list[i][3];
        add_rect(canvas, width=width, height=height, left=left, top=top);
    }

}