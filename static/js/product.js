// Add this to your <script> section
function changeMainImage(newSrc) {
  const mainImg = document.getElementById('mainProductImage');
  mainImg.style.opacity = 0;
  setTimeout(() => {
    mainImg.src = newSrc;
    mainImg.style.opacity = 1;
    mainImg.style.transition = 'opacity 0.3s ease';
  }, 150);
}

// Update your thumbnail onclick attributes to:
onclick="changeMainImage('{{ image.image.url }}')"

// Add this to your existing JavaScript
const mainImg = document.getElementById('mainProductImage');
mainImg.addEventListener('click', function() {
  this.style.transform = this.style.transform === 'scale(1.5)' ? 'scale(1)' : 'scale(1.5)';
});