import { useEffect, useState, useRef } from 'react';

function App() {

  const [symptoms, setSymtoms] = useState([])
  const [resultDiagnose, setResultDiagnose] = useState([]);

  useEffect(() => {
    const getSymptoms = async () => {
      const request = await fetch('http://127.0.0.1:5000/symptoms', {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      });
      const response = await request.json()

      setSymtoms(response)
    }


    getSymptoms()

  }, []);


  function checkedOk(el) {


    const checkbox = el.currentTarget.lastElementChild.children[0];

    if (el.target !== checkbox) {
      checkbox.checked = !checkbox.checked
    }
    // checkbox.checked = !checkbox.checke
  }

  async function diagnose(el) {
    el.preventDefault()
    const formData = new FormData(el.currentTarget);
    const request = await fetch('http://127.0.0.1:5000/diagnose', {
      method: 'POST',
      body: formData
    })
    let result = await request.json()
    result = result.map(value => value[1])
    fetch('http://127.0.0.1:5000/clear', {
      method: 'DELETE',
    }).then(response => console.log(response))
    const gejala = [];
    const symptomsFromInput = Array.from(formData).map((value, index) => value[1])

    symptomsFromInput.forEach((value, index) => {
      symptoms.forEach((symptomp, index) => {
        if (symptomp[0] === value) {
          gejala.push(symptomp[1])
        }
      })
    })
    setResultDiagnose([gejala, result]);
    console.log(resultDiagnose)
  }


  function resetInput(el) {
    const form = el.currentTarget.parentElement.parentElement;
    const listForm = form.querySelectorAll("[name='symptoms[]']");

    listForm.forEach((el) => {
      el.checked = false
      setResultDiagnose([])
    })
  }

  return (
    <div>
      <header className='grid grid-rows-2 mt-3'>
        <h1 className='text-2xl text-slate-700 text-center'>Sistem Pakar Indentifikasi Penyakit Tanaman Cabai</h1>
        <p className='text-center text-xl text-slate-600'>Menggunkan Metode Forward Chaining</p>
      </header>
      <main className='container flex flex-col justify-center m-auto mt-6 mb-16 w-[80%]'>
        <form action="post" className='flex flex-col w-full justify-around' onSubmit={diagnose.bind(this)}>
          <table className='w-full border border-collapse [&>thead>th]:border [&>thead>th]:border-slate-200 [&>tbody>tr>td]:border my-4 [&>thead>th]:p-2 [&>tbody>tr>td]:p-2 rounded-lg'>
            <thead>
              <th>Kode Gejala</th>
              <th>Gejala</th>
              <th>Pilih</th>
            </thead>
            <tbody>
              {symptoms.map((value, index) =>
                <tr key={index} className='cursor-pointer hover:bg-slate-100 transition-all' onClick={checkedOk.bind(this)}>
                  <td>{value[0]}</td>
                  <td>{value[1]}</td>
                  <td className='text-center'><input type="checkbox" name="symptoms[]" id="symptoms" value={value[0]} className='w-10 cursor-pointer' /></td>
                </tr>
              )}
            </tbody>
          </table>
          <div className='flex self-end gap-2'>
            <button type='button' onClick={resetInput.bind(this)} className='px-4 py-2 bg-red-600 rounded-lg text-white hover:bg-red-700  max-w-[300px] font-semibold'>Reset</button>
            <button type='submit' className='px-4 py-2 bg-green-600 rounded-lg text-white hover:bg-green-700  max-w-[300px] font-semibold'>Tampilkan diagnosa</button>
          </div>
        </form>
        <div className='w-full p-4 bg-green-100 mt-2 rounded-lg'>
          {(resultDiagnose[0]) ? (
            <>
              <h5 className='text-slate-950 text-lg'>Gejala Tanaman</h5>
              {resultDiagnose[0].length ?
                <ul className='ml-2'>
                  {resultDiagnose[0].map((value, index) => <li className='text-slate-800 text-sm'>{index + 1}. {value}</li>)}
                </ul> : <p className='ml-2 text-red-500'>Tidak ada gejala</p>}
              <hr className='mt-2' />
              <p>Tanaman mengalami penyakit: <span className='text-red-600'>{(resultDiagnose[1].length) ? resultDiagnose[1].join(', ') : 'Tidak dikenali'}</span></p>
            </>
          ) : 'Belum melakukan diagnosa'}

        </div>
      </main >
    </div >
  );
}

export default App;