
let image_main = document.querySelector("#image-main");

let palette = document.querySelector("#palette");
let linecolor = document.querySelector("#linecolor");
let rect = document.querySelector('#rect');

let ww = document.querySelector("#ww");
let wl = document.querySelector("#wl");
let inverse = document.querySelector('#image-inverse');
let img_form = document.querySelector('#img-form');

const canvas = new fabric.Canvas('image-main', {
    width: 512,
    height: 512
});


mi_fetch();
fabric_setting();

function mi_fetch() {
    let url = "/api/mi/data";
    fetch(url).then(response => response.json())
        .then((result)=>{
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

function add_rect(canvas){
    const rect = new fabric.Rect({
        width: 40,
        height: 40,
        left: 50,
        top: 50,
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


function inverse_change() {
    if (image_inverse.value === "1") {
        image_inverse.value = "0";
    } else if (image_inverse.value === "0") {
        image_inverse.value = "1";
    }
    console.log(image_inverse.value);
}


ww.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        // this.form.submit();
        }
    }
);


wl.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        // this.form.submit();
        }
    }
);


inverse.addEventListener("click",function(event){
    event.preventDefault();
    // this.form.submit();
    // inverse_change();
})


linecolor.addEventListener('change',function(){
    console.log(linecolor.value);
})


rect.addEventListener('click',function(){
    add_rect(canvas);
})

