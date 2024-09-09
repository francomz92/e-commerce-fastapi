const requestWithFiles = async () => {
  const $form = document.getElementById('new-products')
  const formData = new FormData($form)

  try {
    const response = await fetch('http://localhost:8000/api/v1/store/products', {
      method: 'POST',
      body: formData,
    })
    const responseData = await response.json()
    if (response.ok) {
      return responseData
    } else {
      alert(response.status)
    }
  } catch (error) {
    console.log('Error: ', error)
  }
}

const request = async () => {
  const $form = document.getElementById('new-products')
  const formData = new FormData($form)

  try {
    const response = await fetch('http://localhost:8000/api/v1/store/products', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const responseData = await response.json()
    if (response.ok) {
      console.log(responseData)
    } else {
      alert(response.status)
    }
  } catch (error) {
    console.log('Error: ', error)
  }
}

function sendMessage(event) {
  event.preventDefault()
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('Mensaje de prueba')
  }
}
