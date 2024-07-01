// Declare various document elements
const mobileNav = document.querySelector('.mobile-nav-wrapper');
const collapseIcon = document.querySelector('.collapse-icon');

// Event listener for mobile nav icon, opens and closes menu
collapseIcon.addEventListener('click', (e) =>  {
    if (mobileNav.style.display === 'none' 
        || mobileNav.style.display === '') {
        mobileNav.style.display = 'block';
    } 
    else 
    {
        mobileNav.style.display = 'none';
  
    }
    
});
