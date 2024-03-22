let sideMenu = document.querySelectorAll(".nav-link")



sideMenu.forEach(item =>{
    let li = item.parentElement;
    item.addEventListener('click', ()=>{
        sideMenu.forEach((link) =>{
            link.parentElement.classList.remove('active');
        });
        li.classList.add('active');
    })
})

let menuBtn = document.querySelector(".menu-btn");
let sideBar = document.querySelector(".sidebar");
menuBtn.addEventListener("click", ()=>{
    sideBar.classList.toggle("hide");
});

let switchMode = document.getElementById('switch-mode');
switchMode.addEventListener('change', (e)=>{
    if (e.target.checked){
        document.body.classList.add('dark');
    } else{
        document.body.classList.remove('dark');
    }
});

let searchForm = document.querySelector(".content nav form")
let searchBtn = document.querySelector('.search-btn')
let searchIcon = document.querySelector(".search-icon")
searchBtn.addEventListener("click", (e) =>{
    if(window.innerWidth < 576){
        e.preventDefault();
        searchForm.classList.toggle("show");

        if (searchForm.classList.contains("show")){
            searchIcon.classList.replace("fa-search", "fa-times");
        } else{
            searchIcon.classList.replace("fa-times", "fa-search");
        }
    }
});

let tabs = document.querySelectorAll(".tab_btn");
let contents = document.querySelectorAll(".tab-content");
tabs.forEach((tab, index)=>{
    tab.addEventListener("click", (e)=>{
        tabs.forEach((tab)=>{
            tab.classList.remove("active")
        });
        tab.classList.add("active");

    contents.forEach((content)=>{
        content.classList.remove("active")
    });
    contents[index].classList.add("active");
    })
});


window.addEventListener("resize", ()=>{

    if(window.innerWidth > 576){
        searchIcon.classList.replace("fa-times", "fa-search");
    }

    if(window.innerWidth < 768){
        sideBar.classList.add('hide');
    }
});

if (window.innerWidth < 768){
    sideBar.classList.add('hide');
}