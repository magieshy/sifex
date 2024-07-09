const renderExpensesChart = (data, labels) => {
    const ctx1 = document.getElementById("chart-1").getContext("2d");
    const myChart = new Chart(ctx1, {
      type: "polarArea",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last month expenses",
            data: data,
            backgroundColor: [
              "rgba(54, 162, 235, 1)",
              "rgba(255, 99, 132, 1)",
              "rgba(255, 206, 86, 1)",
            ],
          },
        ],
      },
      options: {
        responsive: true,
        
      },
    });
  
  
  
  }
  
  
  const renderMasterAwbChart = (data, labels) => {
    const ctx2 = document.getElementById("masterawb_charts").getContext("2d");
    const myChart2 = new Chart(ctx2, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Incomes Per Source",
            data: data,
            backgroundColor: [
              "rgba(54, 162, 235, 1)",
              "rgba(255, 99, 132, 1)",
              "rgba(255, 206, 86, 1)",
            ],
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }
  
  
  const getSlaveAwbChartData = () => {
    fetch('/expenses_category_summary/').then(res=>res.json()).then((results)=>{
      console.log('results', results)
  
      const category_data = results.expense_category_data
  
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ]
  
      renderSlaveAwbChart(data, labels)
    })
  }
  
  const getMasterAwbChartData = () => {
    fetch('/sifex/total_master_awb_kg/').then(res=>res.json()).then((results)=>{
      console.log('results', results)
  
      const awb_type_data = results.awb_type_data
  
      const [labels, data] = [
        Object.keys(awb_type_data),
        Object.values(awb_type_data),
      ]
  
      renderMasterAwbChart(data, labels)
    })
  }
  
  document.onload = getMasterAwbChartData()
  document.onload = getSlaveAwbChartData()