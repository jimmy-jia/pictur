function updateUpload(i) {
	document.getElementById("fileUpload-text").value = i.value.replace("C:\\fakepath\\", "");
};
function showUpload(){
	var div = $("#upload-section");
	var modal = $("#modal");
	if(div.is(":hidden")){
		$(".login").fadeOut(400, function(){$(".login").remove()});
		div.fadeIn(400);
		modal.fadeIn(400);
	} else {
		div.fadeOut(400);
		modal.fadeOut(400);
	}
}
function handleSearch(event){
	if(event.keyCode === 13){
		window.location.href = "http://pictur.ml:2086/search?tag="+$("#search-box")[0].value;
	}
	return false;
}
function showReply(i){
	console.log($(i).parent());
	if($(i).parent().has("> div.comment-reply-wrapper").length == 0){
		$('<div class="comment-reply-wrapper"><form action="" method=post enctype=multipart/form-data><input type="hidden" name="parentcid" value="'+$(i).parent()[0].attributes["data-commentid"].value+'"></input><textarea required title="Please enter a comment!" name="content"></textarea><button type="submit" name="source" value="comment" class="post-button">Post</button></form></div>').insertAfter($(i).parent().children(".comment-reply"));
	}
	else{
		$(i).parent().children("div.comment-reply-wrapper").remove();
	}
}
function showMobileNav(){
	for(var i=3; i<6; i++){
		if(!$('#svg_'+i).attr('class'))
			$('#svg_'+i).attr('class', 'svg_'+i);
		else
			$('#svg_'+i).removeAttr('class');
	}
	$('#navbar').slideToggle(400);
}
function showSignIn(google_url){
	var div = $('<div class="login">' +
					//'<h1>Log In</h1>' +
					'<span onclick="showSignIn()" class="close">' +
						'<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
						    '<path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>' +
						    '<path d="M0 0h24v24H0z" fill="none"/>' +
						'</svg>' +
					'</span>' +
					/*'<form>' +
						'<input required type="text" name=user placeholder="username"/>' +
						'<input required type="password" name=password placeholder="password"/>' +
						'<button type=submit value="login" name="source">Log In</button>' +
					'</form>' +*/
                    '<a class="google-signin-link" href=\'' + google_url + '\'><img class="google-signin-button" src="static/resources/transparent.gif"/></a>' + 
				'</div>');
	var modal = $("#modal");
	if(modal.is(":hidden") || $("#upload-section").is(":visible")){
		$("#upload-section").fadeOut(400);
		div.insertAfter($("#main"));
		modal.fadeIn(400);
	} else {
		$(".login").fadeOut(400, function(){$(".login").remove()});
		modal.fadeOut(400);
	}
}
function editComment(i){
	if($(i).parent().has(".comment-edit-form").length == 0){
		$(i).parent().children("p.comment-text").hide();
		$('<form class="comment-edit-form" action="" method=post enctype=multipart/form-data>' +
			'<input type="hidden" name="cid" value="'+$(i).parent()[0].attributes["data-commentid"].value+'"></input>' +
			'<textarea required title="Please enter a something!" name="content">'+$(i).parent().children("p.comment-text")[0].innerText+'</textarea>' +
			'<button type="submit" name="source" value="commentedit" class="post-button">Post</button>' +
		'</form>').insertAfter($(i).parent().children(".comment-datetime"));
	}
	else{
		$(i).parent().children(".comment-edit-form").remove();
		$(i).parent().children("p.comment-text").show();
	}
}
function deleteComment(i){

}
function getNextPage(){
	var urlParams = location.search.split('page=')[1];
	if(urlParams){
		window.location.href = "http://pictur.ml:2086?page="+(Number(urlParams)+1);
	}
	else{
		window.location.href = "http://pictur.ml:2086?page=2";
	}
}