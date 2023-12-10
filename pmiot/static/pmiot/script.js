document.addEventListener('DOMContentLoaded', () => {
  const toggleState = () => {
    const button = document.querySelector('.button-turn')
    if (!button) {
      return
    }

    const form = document.querySelector('.change-value')
    if (!form) {
      return
    }

    const input = form.querySelector('#enter_value')
    if (!input) {
      return
    }

      // button.dataset.state = input.value === '' ? 'false' : 'true';
    // button.innerHTML = button.dataset.state;

    // button.addEventListener('click', (evt) => {
    //     // evt.preventDefault();

    //   const isWorking = button.dataset.state === 'True' ? false : true;

    //   input.value = isWorking ? 'True' : '';

    //   button.dataset.state = isWorking ? 'True' : 'False';
    //   button.innerHTML = button.dataset.state;
    //   console.log(isWorking);
    // })

    form.addEventListener('submit', () => {
      const isWorking = button.dataset.state === 'True' ? false : true;
      input.value = isWorking ? 'True' : '';
    })
  }

  toggleState()
})