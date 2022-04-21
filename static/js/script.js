if(window.location.pathname == '/') {
    function hamburgerToggle(){
        let a = document.getElementById('hamburger').classList.toggle('active');
    
    }
    let hamburger_icon = document.getElementById('hamburger');
    hamburger_icon.addEventListener("click", hamburgerToggle );
}

if(window.location.pathname == '/dashboard') {
    function openReceiveFund(){
        document.getElementById("receiveFundOverlay").style.display = "block";
    }
    function closeReceiveFund(){
        document.getElementById("receiveFundOverlay").style.display = "none";
    }
    var receive_fund_btn = document.getElementById("receive_fund_btn");
    var close_receive_btn = document.getElementById("close_receive_btn");
    receive_fund_btn.addEventListener("click", openReceiveFund);
    close_receive_btn.addEventListener("click", closeReceiveFund);
}