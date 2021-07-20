
let login_signup = document.getElementById("login_signup");
let logout = document.getElementById("logout");

let login_mark = document.querySelector(".login_mark");
let login = document.querySelector("#login");
let login_close = document.querySelector("#login_close");
let signup = document.querySelector("#signup");
let signup_close = document.querySelector("#signup_close");
let signup_link = document.querySelector("#signup_link")
let login_link = document.querySelector("#login_link")

let login_form = document.querySelector("#login_form")
let signup_form = document.querySelector("#signup_form")
let login_message = document.querySelector("#login_message")
let signup_message = document.querySelector("#signup_message")

let member = document.querySelector("#member")

login_signup.addEventListener("click", show_1)
login_close.addEventListener("click",close_1)
signup_close.addEventListener("click",close_2)

signup_link.addEventListener("click",show_2)
login_link.addEventListener("click",show_1)

login_form.addEventListener("click", message_clear)
signup_form.addEventListener("click", message_clear)


function show_1() {
    login_mark.style.display = "block";
    login.style.display = "flex";
    signup.style.display = "none";
}

function show_2() {
    login_mark.style.display = "block";
    signup.style.display = "flex";
    login.style.display = "none";
}

function close_1() {
    login_mark.style.display = "none";
    login.style.display = "none";
}

function close_2() {
    login_mark.style.display = "none";
    signup.style.display = "none";
}

login_mark.addEventListener("click", event => {
    let et = event.target;
    if (!login.contains(et) && !signup.contains(et)) {
        login.style.display = "none";
        signup.style.display = "none";
        login_mark.style.display = "none";
    }
});

function message_clear(){
    login_message.textContent = "";
    signup_message.textContent = "";
}


// user_api
const user_url = "/api/user";

// GET
user_get()

function user_get(){
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            // login_signup.innerText = "登出系統";
            // login_signup.textContent = "登出系統";
            login_signup.classList.add("blockhide");
            logout.classList.remove("blockhide");
            member.textContent = `${data.data["name"]}，您好`;
            console.log(data);
        } else {
            // console.log(location.href);
            // console.log(window.location.pathname);
            console.log(data);
            if (window.location.pathname !== "/") {
                document.location.href="/";
            }
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

// POST
signup_form.addEventListener("submit", e => {
    e.preventDefault();
    user_signup();
})

function user_signup(){
    let signup_name = document.querySelector("#signup_name");
    let signup_email = document.querySelector("#signup_email");
    let signup_password = document.querySelector("#signup_password");
    let data = {
        "name": signup_name.value,
        "email": signup_email.value,
        "password": signup_password.value
    };

    fetch(user_url,{
        method:'POST',
        body:JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            console.log(data);
            signup_message.textContent = "註冊成功";
            setTimeout(show_1, 2000);
        } else if (data.error) {
            console.log(data);
            signup_message.textContent = data.message;
        }
        clear_input();
    })
    .catch((error) => {
        console.log("err:", error)
    });
}


// PATCH
login_form.addEventListener("submit", e => {
    e.preventDefault();
    user_login();
})

function user_login(){
    let login_email = document.querySelector("#login_email");
    let login_password = document.querySelector("#login_password");
    let data = {
        "email": login_email.value,
        "password": login_password.value
    };

    fetch(user_url,{
        method:'PATCH',
        body:JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            login_signup.classList.add("blockhide");
            logout.classList.remove("blockhide");
            console.log(data);
            login_message.textContent = "登入成功";
            user_get();
            setTimeout(close_1, 1000);
        } else if (data.error) {
            console.log(data);
            login_message.textContent = data.message;
        }
        clear_input();
    })
    .catch((error) => {
        console.log("err:", error)
    });
}


// DELECT
logout.addEventListener("click", user_logout)

function user_logout(){
    fetch(user_url,{method:'DELETE'}).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            logout.classList.add("blockhide");
            login_signup.classList.remove("blockhide");
            member.textContent = "";
            document.location.href="/";
            console.log(data);
        } 
    })
    .catch((error) => {
        console.log("err:", error)
    });
    message_clear();
}


function clear_input() {
    let clear = document.querySelectorAll(".input")
    clear.forEach(element => {
        element.value = ""
    });
}

let membercheck = document.querySelector("#membercheck")

membercheck.addEventListener("click", member_link)

function member_link() {
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            document.location.href="/member";
        } else {
            show_1();
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

let maincheck = document.querySelector("#maincheck")

maincheck.addEventListener("click", main_link)

function main_link() {
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            document.location.href="/main";
        } else {
            show_1();
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}