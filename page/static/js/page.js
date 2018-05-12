$("upvotes").click(function() {
	var clubid;
	var reveiwid;
	clubid = $(this).attr(data-clubid);
	reviewid = $(this).attr(data-reviewid);
	$.get('page/review_increment/', {pk_Club=clubid, pk_Review=reviewid}, function(data) {
		$('#vote_count').html(data);
		$('#upvotes').hide();
	});
});