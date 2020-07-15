document.addEventListener("DOMContentLoaded", function() {
    window.addEventListener("load", function() {
        var forms = document.getElementsByClassName("needs-validation");
        var validation = Array.prototype.filter.call(forms, function(form) {

            if (form.id === 'register') {
                form.addEventListener('keyup', function() {

                    $.get("/check?username=" + form.username.value, function(data) {
                        if (data) {
                            document.querySelector("#invalid-username").innerHTML = "Username may not be left blank.";
                            form.username.setCustomValidity("");
                        }
                        else {
                            document.querySelector("#invalid-username").innerHTML = "Username is unavailable.";
                            form.username.setCustomValidity("invalid");
                        }
                    });

                    $.get("/check?email=" + form.email.value, function(data) {
                        if (data) {
                            document.querySelector("#invalid-email").innerHTML = "Invalid email.";
                            form.email.setCustomValidity("");
                        }
                        else {
                            document.querySelector("#invalid-email").innerHTML = "User with this email already exists.";
                            form.email.setCustomValidity("invalid");
                        }
                    });

                    if (form.password.value != form.confirmation.value) {
                        form.confirmation.setCustomValidity('invalid');
                    }
                    else {
                        form.confirmation.setCustomValidity("");
                    }
                });
            }

            if ((form.id.startsWith("reg-pizza") || form.id.startsWith("sic-pizza")) && !form.id.endsWith("Cheese")) {
                form.addEventListener('click', function() {
                    var expected_toppings;
                    if (form.id.endsWith("1topping") || form.id.endsWith("1item")) {
                        expected_toppings = 1;
                    }
                    else if (form.id.endsWith("2toppings") || form.id.endsWith("2items")) {
                        expected_toppings = 2;
                    }
                    else if (form.id.endsWith("3toppings") || form.id.endsWith("3items")) {
                        expected_toppings = 3;
                    }
                    else if (form.id.endsWith("Special")) {
                        expected_toppings = 4;
                    }

                    var selected_toppings = Math.min(4, form.querySelectorAll("input[name='topping_ids']:checked").length);
                    if (expected_toppings !== selected_toppings) {
                        form.toppings.setCustomValidity("invalid");
                    }
                    else {
                        form.toppings.setCustomValidity("");
                    }
                });
            }

            form.addEventListener("submit", function(event) {
                if (form.checkValidity() === false) {
                    if (form.id === 'register') {
                        document.querySelector('small').style.display = "none";
                    }
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add("was-validated");
            });

        });
    });

    var navOrders = document.querySelector("#orders")
    if (window.location.href.endsWith("/orders")) {
        navOrders.classList.add("active")
    }
    else {
        navOrders.classList.remove("active")
    }

    document.querySelectorAll(".clickable").forEach(function(row) {
        row.onclick = function() {
            $(".collapse").collapse("hide");
        };
    });

    var checkoutBtn = document.querySelector("#checkout")
    if (checkoutBtn) {
        checkoutBtn.onclick = function() {
            $.get("/stripe_session", function(data) {
                var stripe = Stripe(data.stripe_public_key);
                stripe.redirectToCheckout({
                    sessionId: data.session_id
                });
            })
        };
    }

});
