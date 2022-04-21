<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>WaPay - User Dashboard</title>
	<link rel="stylesheet" type="text/css" href="/assets/css/style.css">

	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta2/css/all.min.css" integrity="sha512-YWzhKL2whUzgiheMoBFwW8CKV4qpHQAEuvilg9FAn5VJUDwKZZxkJNuGM4XkWuk94WCrrwslk8yWNGmY1EduTA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
	<div class="dashboard-container">
		<nav class="sidebar">
			<div class="logo">
				<h4 class="logo-text">WaPay Wallet</h4>
				<div class="logo-img">
					<img src="https://image.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg">
				</div>
				<div class="welcome-text">Welcome, <br> {{ $user->name }}</div>
			</div>
			<ul class="page-links">
				<li>
					<a href="#"><i class="fas fa-th-large"></i> Dashboard</a>
				</li>
				<li>
					<a href="#"><i class="fas fa-exchange-alt"></i> Transactions</a>
				</li>
				<li>
					<a href="#"><i class="fas fa-wallet"></i> Wallet</a>
				</li>
				<li>
					<a href="#"><i class="fas fa-credit-card"></i> Fund Wallet</a>
				</li>
				<li>
					<a href="#"><i class="fas fa-money-bill-wave"></i> Pay Bills</a>
				</li>
				<li>
					<a href="#"><i class="fas fa-dollar-sign"></i> Currency Rate</a>
				</li>
			</ul>
		</nav>
		<div class="content">
			<nav class="content-nav">
				<div class="input-wrapper">
					<input id="stuff" placeholder="Test">
					<label for="stuff" class="input-icon"><i class="fas fa-search"></i></label>
				</div>

				<div class="">
					<span class="notification">
						<a href=""><i class="fas fa-bell"></i></a>
					</span>
					<span class="profile-img">
						<img src="https://image.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg">
					</span>
				</div>
			</nav>
			<div class="content-body">
				
                <form action="">
                    <input  id="amount" name="amount" value="3000">
                    <input type="email" id="email" name="email" placeholder="email" value="customer@gmail.com">
                    <input type="text" id="phone" placeholder="phone number" name="phone" value="08012345678">
                    
                    <button type="button" onClick="makePayment()">Pay Now</button>
                  </form>

				
			</div>
		</div>
	</div>








	<script src="assets/js/script.js"></script>
    <script src="https://checkout.flutterwave.com/v3.js"></script>
      
      <script>
        const amount = document.getElementById('amount').value;
        function makePayment() {
          FlutterwaveCheckout({
            public_key: "{{ env('FLUTTERWAVE_TEST_PUBLIC_KEY') }}",
            tx_ref: "WP-{{ mt_rand() }}",
            currency: "NGN",
            amount: amount,
            redirect_url: "http://127.0.0.1:8000/wallet/",
            customer: {
                email: "{{ Auth::user()->email }}",
                // phone_number: "{{ Auth::user()->phone }}",
                phone_number: "09090909090",
                name: "{{ Auth::user()->first_name.' '.Auth::user()->last_name }}",
            },
            customizations: {
                title: "{{ env('APP_NAME') }}",
                description: "Wallet Deposit",
                logo: "https://www.iconsdb.com/icons/preview/blue/money-bag-xxl.png",
            },
            callback: function (data) {
              console.log(data);
            },
          });
        }
      </script>
      
</body>
</html>