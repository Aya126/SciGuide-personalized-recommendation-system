const grade = document.querySelector("#\grade");
const tbody = document.querySelector("#tbody");
const tfoot = document.querySelector("#tfoot");
var shoppingCart = (function () {
  
    let cart = [];
    function Item(name, price,count ) {
      this.name = name;
      this.price = price;
      this.count = count;
    
    }

    // Save cart
    function saveCart() {
      localStorage.setItem('shoppingCart', JSON.stringify(cart));
    }

    // Load cart
    function loadCart() {
      cart = JSON.parse(localStorage.getItem('shoppingCart'));
    }
    if (localStorage.getItem("shoppingCart") != null) {
      loadCart();
    }


    var obj = {};

    // Add to cart
    obj.addItemToCart = function (name, price, count) {
      for (var item in cart) {
        if (cart[item].name === name) {
          alert("This item is already added to the gpa!");
          return;
        }
      }
      var item = new Item(name, price, count);
      cart.push(item);
      saveCart();
    }
    // Set count from item
    obj.setCountForItem = function (name, count) {
      for (var i in cart) {
        if (cart[i].name === name) {
          if(Math.sign(count) === -1){
            cart.splice(i, 1);
            saveCart();
            break;
          }
          else{
            cart[i].count = count;
            break;
          }
        }
      }
    };

// // Remove all items from cart
  // obj.removeItemFromCartAll = function(name) {
  //   for(var item in cart) {
  //     if(cart[item].name === name) {
  //       cart.splice(item, 1);
       
  //       return;
  //     }
  //   }
  //   saveCart();
  // }

    // Clear cart
    obj.clearCart = function () {
      cart = [];
      saveCart();
    }

    // Count cart 
    obj.totalCount = function () {
      var totalCount = 0;
      for (var item in cart) {
        totalCount += 1;
      }
      return totalCount;
    }

   // Total cart
    obj.totalCart = function () {
      var gpa,
          totalCart = 0,
          newprice = 0;
      for (var item in cart) {
        newprice += cart[item].price;
        totalCart += cart[item].price * cart[item].count;
      }
      gpa = Number((totalCart/newprice).toFixed(2));
      return gpa
    }

    
    // List cart
    obj.listCart = function () {
      var cartCopy = [];
      for (i in cart) {
        item = cart[i];
        itemCopy = {};
        for (p in item) {
          itemCopy[p] = item[p];
        }
        itemCopy.total = Number(item.price * item.count).toFixed(2);
        cartCopy.push(itemCopy)
      }
      return cartCopy;
    }
    return obj;
  })();


  // Add item
  $('.default-btn').click(function (event) {
    // alert('working');
    event.preventDefault();
    var name = $(this).data('name');
    var price = Number($(this).data('price'));
    shoppingCart.addItemToCart(name, price, 0);
    displayCart();
  });

  // Clear items
  $('.clear-cart').click(function () {
    shoppingCart.clearCart();
    displayCart();
  });
  
  function findEligibility(gpa) {
    let greetingsText;

    if (gpa >= 3.7) {
        greetingsText = "EXCELLANT!";
    } else if (gpa >= 3.3) {
        greetingsText = "Very Good!";
    } else if (gpa >= 3.0) {
              greetingsText = "Good!";
    } else if (gpa >= 2.0) {
        greetingsText = "Hmmm...";
    } else if(gpa >= 0.0){
        greetingsText = "Sorry!";
    } else{
      greetingsText = "Hello";
    }

    return greetingsText;
}


function findEligibility2(gpa) {
  let eligibilityText;

  if (gpa >= 3.7) {
      eligibilityText = 'You are maintaining "First Class" degree. Keep it up!';
  } else if (gpa >= 3.3) {
      eligibilityText =
          'Currently you are in "Second Upper" degree level. Try little bit more to go to the "First Class".';
  } else if (gpa >= 3.0) {
      eligibilityText =
          'Currently you are in "Second Lower" degree level. Keep going.';
  } else if (gpa >= 2.0) {
      eligibilityText =
          'Is "General Degree" enough for you? Work Hard! You can do better.';
  } else if (gpa >= 0.0) {
      eligibilityText = "Currently you are not eligible for the degree.";
  }
  else{
    eligibilityText = "Waiting for calculations..."
  }

  return eligibilityText;
    
}


  function displayCart() {
    var cartArray = shoppingCart.listCart();
    var output = "";
    for (var i in cartArray) {
      
      output += "<tr>"
      +"<td>" + cartArray[i].name + "</td>"
        + "<td>(" + cartArray[i].price + ")</td>"
        //+ "<td>(" + grade.options[grade.selectedIndex].value + ")</td>"
        + "<td><div class='input-group'>"
    //  + "<div class='col s12 m3 input-field'>"
     +"<select class='item-count form-control' data-name='" + cartArray[i].name + "' value='" + cartArray[i].count + "'>"
     +"<option id='red' value='none' selected>Select Grade</option>"
     +"<option id='red' value='4.00'>A</option>"
     +"<option id='red' value='3.67'>A-</option>"
     +"<option id='red'value='3.33'>B+</option>"
     +"<option value='3.00'>B</option>"
     +"<option value='2.67'>B-</option>"
     +"<option value='2.33'>C+</option>"
     +"<option value='2.00'>C</option>"
     +"<option value='1.67'>C-</option>"
     +"<option value='1.33'>D+</option>"
     +"<option value='1.00'>D</option>"
     +"<option value='0'>F</option>"
     +"<option value='-1' style='background-color: #c42915; cursor: pointer;color: #fff;font-weight:bold;text-align:center'>remove</option>"        

    + "</select>"
    + "<input  class='item-count form-control'  readonly  value='" + cartArray[i].count + "'>"
         + "<td>" + cartArray[i].total + "</td>"
    +"</tr>";
    }
    
    $('.show-cart').html(output);
    var res = shoppingCart.totalCart();
    $('.total-cart').html(res);
    $('.talking').html(findEligibility(res));
    $('.total-cart').html(res);
    $('.talking2').html(findEligibility2(res));
    $('.total-count').html(shoppingCart.totalCount());
    if (res >= 3.7) {
      $('.talking').css('color', '#6b8e23');
      $('.talking2').css('color', '#6b8e23');
      $('.bi-mortarboard').css('color', '#6b8e23');
    } else if (res >= 3.3) {
      $('.talking').css('color', 'teal');
      $('.talking2').css('color', 'teal');
      $('.bi-mortarboard').css('color', 'teal');
    } else if (res >= 3.0) {
      $('.talking').css('color', '#000080');
      $('.talking2').css('color', '#000080');
      $('.bi-mortarboard').css('color', '#000080');
    } else if (res >= 2.0) {
      $('.talking').css('color', '#8b4513');
      $('.talking2').css('color', '#8b4513');
      $('.bi-mortarboard').css('color', '#8b4513');
    } else if(res >= 0.0){
      $('.talking').css('color', 'red');
      $('.talking2').css('color', 'red');
      $('.bi-mortarboard').css('color', 'red');
    } else{
      $('.talking').css('color', '#183d69');
      $('.talking2').css('color', '#183d69');
      $('.bi-mortarboard').css('color', '#183d69');
    } 
  }

  // Item count input
  $('.show-cart').on("change", ".item-count", function (event) {
    var name = $(this).data('name');
    var count = Number($(this).val());
    shoppingCart.setCountForItem(name, count);
    displayCart();
  });

  displayCart();

//////// ui script start /////////
// Tabs Single Page
$('.tab ul.tabs').addClass('active').find('> li:eq(0)').addClass('current');
$('.tab ul.tabs li a').on('click', function (g) {
    var tab = $(this).closest('.tab'), 
    index = $(this).closest('li').index();
    tab.find('ul.tabs > li').removeClass('current');
    $(this).closest('li').addClass('current');
    tab.find('.tab_content').find('div.tabs_item').not('div.tabs_item:eq(' + index + ')').slideUp();
    tab.find('.tab_content').find('div.tabs_item:eq(' + index + ')').slideDown();
    g.preventDefault();
});

jQuery(function() {
  jQuery(".allbutton").click(function(){
      jQuery(".single").show();
  });
  jQuery(".button").click(function(){
      jQuery(".single").hide();
      jQuery(".div"+ $(this).attr('target')).show();
  });
});
/*scroll to top*/
let calcScrollValue = () => {
  let scrollProgress = document.getElementById("progress");
  let progressValue = document.getElementById("progress-value");
  let pos = document.documentElement.scrollTop;
  let calcHeight =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  let scrollValue = Math.round((pos * 100) / calcHeight);
  if (pos > 100) {
    scrollProgress.style.display = "grid";
  } else {
    scrollProgress.style.display = "none";
  }
  scrollProgress.addEventListener("click", () => {
    document.documentElement.scrollTop = 0;
  });
  scrollProgress.style.background = `conic-gradient(#0077b6 ${scrollValue}%, #d7d7d7 ${scrollValue}%)`;
};



window.onscroll = calcScrollValue;
window.onload = calcScrollValue;

const cartButtons = document.querySelectorAll('.default-btn');

cartButtons.forEach(button => {
	button.addEventListener('click', cartClick);
});

function cartClick() {
	let button = this;
	button.classList.add('clicked');
}