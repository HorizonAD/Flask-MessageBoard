// 搜索切换
function Searchtype(value){
  if (value=="post"){
  	document.getElementById("search_form").action="../searchpost"
  }
  else if(value=="comment"){
  	document.getElementById("search_form").action="../searchcomment"
  }
}