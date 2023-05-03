if(window.location.pathname == '/') {
    function hamburgerToggle(){
        let hamburger = document.getElementById('hamburger');
        hamburger.classList.toggle('active');

        let nav_check = hamburger.classList.contains('active');
        
        // If a is active call, open Nav
        // Else call close nav
        if(nav_check){
            openNav();
            disableScroll();
            
        }
        else{
            closeNav();
            enableScroll();
        }
            // openNav()

        
    
    }
    function disableScroll() {
        // Get the current page scroll position
        scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
      
            // if any scroll is attempted, set this to the previous value
            window.onscroll = function() {
                window.scrollTo(scrollLeft, scrollTop);
            };
    }
      
    function enableScroll() {
        window.onscroll = function() {};
    }
    function openNav() {
        document.getElementById("myNav").style.width = "100%";
      }
      
    function closeNav() {
        document.getElementById("myNav").style.width = "0%";
    }
    let hamburger_icon = document.getElementById('hamburger');
    hamburger_icon.addEventListener("click", hamburgerToggle );
}


let currentScrollPositon = 0
let scrollAmount = 320
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









