console.log("JS is running");

        let currentStep = 1;

        function changeStep(step) {
            const totalSteps = 3;
            const steps = document.querySelectorAll('.step');

             let newStep = currentStep + step;

    // Stop if out of range
    if (newStep < 1 || newStep > totalSteps) {
        return;
    }

    // Hide current
    steps[currentStep - 1].classList.remove('active');

    // Update step
    currentStep = newStep;

    // Show new
    steps[currentStep - 1].classList.add('active');

            // Enable/disable navigation buttons
            document.getElementById('prevBtn').disabled = currentStep === 1;
            document.getElementById('nextBtn').classList.toggle('d-none', currentStep === totalSteps);
            document.getElementById('submitBtn').classList.toggle('d-none', currentStep !== totalSteps);

            // Update progress bar
            const progressBar = document.getElementById('progressBar');
            const progress = (currentStep / totalSteps) * 100;
            progressBar.style.width = progress + '%';
            progressBar.setAttribute('aria-valuenow', progress);
            progressBar.setAttribute('data-step', `Step ${currentStep} of ${totalSteps}`);
        }

        // document.getElementById('registrationForm').addEventListener('submit', function (e) {
        //     alert('Form submitted successfully!');
        // });

      
// window.toggleHeart = function(element) {
//     element.classList.toggle("liked");

//     if (element.classList.contains("liked")) {
//         element.textContent = "♥";
//     } else {
//         element.textContent = "♡";
//     }
// }


// window.toggleHeart = function(element, productId) {
    
//     fetch(`/toggle-wishlist/${productId}/`)
//     .then(response => response.json())
//     .then(data => {

//         if (data.status === "added") {
//             element.classList.add("liked");
//             element.textContent = "♥";
//         } else {
//             element.classList.remove("liked");
//             element.textContent = "♡";
//         }
//     });
// }
document.addEventListener("DOMContentLoaded", function () {

let slider = document.getElementById("cardSlider");

let interval;

function updateActive() {
    let slides = document.querySelectorAll(".slide");

    slides.forEach(s => s.classList.remove("active"));

    let centerIndex = Math.floor(slides.length / 2);

    if (slides[centerIndex]) {
        slides[centerIndex].classList.add("active");
    }
}

function autoSlide() {
    // animate slide
    slider.style.transition = "transform 0.5s ease";
    slider.style.transform = "translateX(-300px)";

    setTimeout(() => {
        // move first card to end
        slider.appendChild(slider.children[0]);

        // reset position instantly
        slider.style.transition = "none";
        slider.style.transform = "translateX(0)";

        updateActive();
    }, 500);
}

function startAuto() {
    interval = setInterval(autoSlide, 2500);
}
// start auto sliding
updateActive();
startAuto();

// pause on hover
if (slider) {

    slider.addEventListener("mouseenter", () => {
        clearInterval(interval);
    });

}

// resume
slider.addEventListener("mouseleave", () => {
    startAuto();
});

// manual hover
slider.addEventListener("mouseover", (e) => {
    if (e.target.classList.contains("slide")) {
        let slides = document.querySelectorAll(".slide");

        slides.forEach(s => s.classList.remove("active"));
        e.target.classList.add("active");
    }
});
})

// document.addEventListener("DOMContentLoaded", function () {

//     const raw = document.getElementById("products-data").textContent.trim();
//     console.log("RAW:", raw);

//     const products = JSON.parse(raw);

//     console.log("PARSED:", products);

//     const container = document.getElementById("card-container");

//     let index = 0;

//     function showCards() {
//         container.innerHTML = "";

//         for (let i = 0; i < 2; i++) {
//             let product = products[(index + i) % products.length];

//             console.log("PRODUCT:", product);

//             let card = document.createElement("div");
//             card.className = "new-card " + (i % 2 === 0 ? "card-left" : "card-right");

//             let imgSrc = product.image || "https://via.placeholder.com/150";

//             card.innerHTML = `
//                 <img src="${imgSrc}" style="width:300px; height:300px;">
//             `;

//             container.appendChild(card);
//         }

//         index = (index + 2) % products.length;
//     }

//     if (products.length > 0) {
//         showCards();
//         setInterval(showCards, 5000);
//     }

// });

document.addEventListener("DOMContentLoaded", function () {

    const products = JSON.parse(document.getElementById("products-data").textContent);

    const latestProducts = products.slice(0, 10);

    let index = 0;

    const leftSlot = document.getElementById("left-slot");
    const rightSlot = document.getElementById("right-slot");

    function createCard(product, side) {
        return `
            <a href="/customer/product/${product.id}/" class="card-link ${side}-animate">
                <div class="card">
                    <img src="${product.image}" alt="${product.name}">
                    <h4>${product.name}</h4>
                </div>
            </a>
        `;
    }

    function showCards() {
        if (!leftSlot || !rightSlot) {
            console.error("Slots not found!");
            return;
        }

        const leftProduct = latestProducts[index % latestProducts.length];
        const rightProduct = latestProducts[(index + 1) % latestProducts.length];

        leftSlot.innerHTML = createCard(leftProduct, "left");
        rightSlot.innerHTML = createCard(rightProduct, "right");

        index += 2;
    }

    showCards();
    setInterval(showCards, 6000);
});

/*product-detail page*/
let currentIndex = 0;

const images = document.querySelectorAll(".slider-image");
const dots = document.querySelectorAll(".dot");

function showImage(index){

    images.forEach(img => img.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active-dot"));

    images[index].classList.add("active");
    dots[index].classList.add("active-dot");
}

function nextImage(){
    currentIndex++;
    if(currentIndex >= images.length){
        currentIndex = 0;
    }
    showImage(currentIndex);
}

function prevImage(){
    currentIndex--;
    if(currentIndex < 0){
        currentIndex = images.length - 1;
    }
    showImage(currentIndex);
}

function goToImage(index){
    currentIndex = index;
    showImage(currentIndex);
}

// login msg
document.addEventListener("DOMContentLoaded", function () {
    const toasts = document.querySelectorAll(".ruhava-toast");
    if (toasts.length > 0) {
        setTimeout(() => {
            toasts.forEach(toast => {
                toast.style.transition = "0.5s";
                toast.style.opacity = "0";

                setTimeout(() => {
                    toast.remove();
                }, 500);
            });
        }, 3000);
    }
});