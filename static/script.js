

function autoSuggest(){

    searchInput = document.getElementById('search');
    query = searchInput.value

    fetch(`http://127.0.0.1:5000/autocomplete/${query}`).then(res => res.json()).then(result=>{

        availableTags = result['data']
            $( "#search" ).autocomplete({
                  source: availableTags
            });
    })
    
}
function saveQueryForSuggestion(){
    console.log("saving the query in the savaeQueryFOrSuggestion")
  

    searchInput = document.getElementById('search');
    query = searchInput.value
    query = query.replaceAll(" ", "-")
    fetch(`http://127.0.0.1:5000/autocomplete/${query}`,  {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"data": query})
      })
      .then(res => console.log(res))
      // console.log("returning false")
      // return false
      
}

//ob = {"a":1,"about":1,"is":1,"the":1,"that":1,"and":1,"i":1,"from":1,"of":1,"with":1,"an":1,"in":1,"on":1,"for":1,"to":1}
stopwords = ['a', 'about', 'is', 'the', 'that', 'and', 'i', 'from', 'of', 'with', 'an', 'in', 'on', 'for', 'to' ]

function isNotStopword(w){
  //if(ob[w]!= undefined) return false
  if (stopwords.includes(w)) return false 
  return true
}


function highligherTest(){
  let keywordsString = (document.getElementById('search').value).trim().split(' ').filter(isNotStopword).join(' ')
  console.log(keywordsString)
  let keywords = keywordsString.split('');
  
  let pattern = new RegExp(`(${keywords.join('|')})`, 'gi'); 
  results = document.querySelectorAll('.boxa')
  for (let i =0; i < results.length; i ++){  
    results[i].innerHTML = (results[i].textContent).replace(pattern, match => `<mark>${match}</mark>`)
  }

}
function highlight(){
  
  let keywords = (document.getElementById('search').value).trim().split(' ').filter(isNotStopword)
  let pattern = new RegExp(`(${keywords.join('|')})`, 'gi'); 
  results = document.querySelectorAll('.boxa')
  for (let i =0; i < results.length; i ++){  
    results[i].innerHTML = (results[i].textContent).replace(pattern, match => `<mark>${match}</mark>`)
  }

  handleSelectChoice()      
  
  
}

function handleSelectChoice(){


let keyword = `<option value="k">keyword</option>`
let sematnic = `<option value="s">sematnic</option>`

  let selectBox = document.getElementById('select_box')
  if (selectBox==null) console.log('yes its null')

  // loading 
  let selectedSearchType = sessionStorage.getItem("selected_type");  

  // saving 
  selectBox.addEventListener('change', ()=>{
    sessionStorage.setItem("selected_type", selectBox.value);
    if (selectBox.value == 'k')
      selectBox.innerHTML = keyword + "\n" + sematnic
    else 
      selectBox.innerHTML = sematnic+ "\n" + keyword
  })

  if(selectedSearchType!= null)
  selectBox.value = selectedSearchType
   if (selectBox.value == 'k')
    selectBox.innerHTML = keyword + "\n" + sematnic
  else 
    selectBox.innerHTML = sematnic+ "\n" + keyword
  

}