const colorInput = document.querySelector('#color-input');
const colorData = document.querySelector('#color-data');

const timeInput = document.querySelector('#time-input');
const timeData = document.querySelector('#time-data');

const submit = document.querySelector('button');

const boxContent = document.querySelector('#box-content');

actualizarInput(colorInput, colorData);
actualizarInput(timeInput, timeData);

function actualizarInput(input, data) {
	data.textContent = input.value;
}

colorInput.addEventListener('change', ()=>actualizarInput(colorInput, colorData));
timeInput.addEventListener('change', ()=>actualizarInput(timeInput, timeData));
submit.addEventListener('click', createBox);

function createBox(e) {
	e.preventDefault();
	
	const time = timeInput.value * 1000;

	const h2 = document.createElement('h2');
	h2.style.backgroundColor = colorInput.value;
	if(time<2000){
		h2.textContent = `This box will be autodestrioed in ${timeInput.value} second!`;
	} else {
		h2.textContent = `This box will be autodestrioed in ${timeInput.value} seconds!`;
	}

	boxContent.appendChild(h2);

	setTimeout(()=>h2.remove(), time);
}
