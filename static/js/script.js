if(window.location.pathname == '/') {
    function hamburgerToggle(){
        let a = document.getElementById('hamburger').classList.toggle('active');
    
    }
    let hamburger_icon = document.getElementById('hamburger');
    hamburger_icon.addEventListener("click", hamburgerToggle );
}


function getBankList(){

}

let currentScrollPositon = 0
let scrollAmount =320
const sCont = document.querySelector(".menu-icons-container")
const hScroll = document.querySelector(".menu-bar")
const btnScrollLeft =  document.querySelector("#btn-scroll-left")
const btnScrollRight =  document.querySelector("#btn-scroll-right")
btnScrollLeft.style.opacity = "0"

let maxScroll = -sCont.offsetWidth + hScroll.offsetWidth;

function scrollHorizontally(val){
    currentScrollPositon += (val * scrollAmount)

    if(currentScrollPositon >= 0){
        currentScrollPositon = 0
        btnScrollLeft.style.opacity = "0"
    }

    if(currentScrollPositon >= 0){
        currentScrollPositon = 0
        btnScrollLeft.style.opacity = "0"
    }else{
        btnScrollLeft.style.opacity = "1"
    }
    if(currentScrollPositon <= maxScroll){
        currentScrollPositon = maxScroll
        btnScrollRight.style.opacity = "0"
    }else{
        btnScrollRight.style.opacity = "1"
    }
    sCont.style.left = currentScrollPositon+"px"
}