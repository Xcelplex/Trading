var sideBarOpen= false;
var sidebar = document.getElementById("sidebar")

function openSidebar(){
    if(!sideBarOpen){
    sidebar.classList.add("sidebar-responsive");
    sideBarOpen = True;
    }
}

function closeSideBar(){
    if(sideBarOpen){
        sideBarOpen.bar.classList.add("sidebar-responsive");
        sideBarOpen = False;
    }
}