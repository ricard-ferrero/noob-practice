const resBox = document.querySelector("#result");
const btnNum = document.querySelectorAll('.n')
const btnOp = document.querySelectorAll('.o')
const btnDot = document.querySelector('.dot')
const btnRes = document.querySelector('.eq')

let result = 0;
let savedNum = 0;
let operator = ''

eventListeners();

function eventListeners() {
	btnNum.forEach( btn => {
		btn.addEventListener('click', setNum);
	});

	btnOp.forEach( btn => {
		btn.addEventListener('click', operating);
	});

	btnRes.addEventListener('click', setResult);
}

function setNum(e) {
	if(operator=='='){
		operator='';
		result = 0;
	}
	const number = parseInt(e.target.textContent);
	const x = result*10 + number;
	if(x <= 99999999999){
		result = x;
		resBox.textContent = result;
	}
}

function operating(e) {
	if(operator==''){
		operator = e.target.textContent;
		savedNum = result;
		result = 0;
		return
	}
	if(operator=='='){
		operator = e.target.textContent;
		result = 0;
		return;
	}

	setResult(e);
}

function setResult(e) {
	let x = 0;

	if(operator == '+') {
		x = savedNum + result;	
	}
	if(operator == '-') {
		x = savedNum - result;
	}
	if(operator == 'x') {
		x = savedNum * result;
	}
	if(operator == '÷') {
		x = savedNum / result;
	}

	resBox.textContent = x;
	savedNum = x;
	operator = e.target.textContent;
	result = 0;
}