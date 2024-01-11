let star = document.querySelectorAll('input');
let showValue = document.querySelector('#rating-value');
let resetBtn = document.querySelector('#reset-btn');
let itemId = ''; // Initialize the item ID variable

// Get the user ID or name from some source, such as a login system
// This example assumes that the user ID is stored in a variable called `userId`
let userId = 'user123'; // Replace with the actual user ID or name

// Set the item ID to a unique value based on the user ID or name
itemId = 'item_' + userId;

// Check if there's a saved rating for this user in local storage
const savedRating = localStorage.getItem(itemId);

if (savedRating) {
  // If there's a saved rating, set the rating element to the saved value
  showValue.innerHTML = savedRating + " out of 5";
}

for (let i = 0; i < star.length; i++) {
	star[i].addEventListener('click', function() {
		i = this.value;
		showValue.innerHTML = i + " out of 5";
		
		// Save the rating to local storage
		localStorage.setItem(itemId, i);
	});
}

resetBtn.addEventListener('click', function() {
  // Reset the rating element and remove the saved rating data from local storage
  showValue.innerHTML = "0 out of 5";
  localStorage.removeItem(itemId);
});