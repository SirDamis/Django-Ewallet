<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>WaPay - User Dashboard</title>
	<link rel="stylesheet" type="text/css" href="assets/css/style.css">

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
		</div>
	</div>




	<!-- Receive Funds Overlay -->
	<div id="receiveFundOverlay" class="receive-overlay">
		<a id="close_receive_btn" class="closebtn" onclick="closeNav()">&times;</a>
	
	</div>



	<script src="assets/js/script.js"></script>
</body>
</html>