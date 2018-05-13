$(document).ready(function() {
	$(".upvote").click(function() {
		var view_url = $(this).attr('data-url');
		var review_id = $(this).attr('data-id');
		$.ajax({
	        url: view_url,
	        success: function(data) {
	        	$("#vote_count-" + review_id).html(data);
	        	//$("#up-" + review_id).removeClass().addClass("fas fa-arrow-alt-circle-up");
	        	//$("#down-" + review_id).removeClass().addClass("far fa-arrow-alt-circle-down");
	        }
	    });
	});

	$(".downvote").click(function() {
		var view_url = $(this).attr('data-url');
		var review_id = $(this).attr('data-id');
		$.ajax({
	        url: view_url,
	        type: "GET",
	        success: function(data) {
	        	$("#vote_count-" + review_id).html(data);
	        	//$("#up-" + review_id).removeClass().addClass("far fa-arrow-alt-circle-up");
	        	//$("#down-" + review_id).removeClass().addClass("fas fa-arrow-alt-circle-down");
	        }
	    });
	});

	$(".express").click(function() {
		var view_url = $(this).attr('data-url');
		$.ajax({
	        url: view_url,
	        type: "GET",
	        success: function(data) {
	        	if (data == 0) {
	        		$(".express").html("Express interest!");
	        	}
	        	else {
	        		$(".express").html("Unexpress interest!");
	        	}
	        }
	    });
	});

});