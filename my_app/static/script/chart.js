const data = {
    labels: {{ time_graph | safe }},
    datasets: [{
      label: 'something',
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: {{ value_graph  }},
    }]
  };

  const config = {
    type: 'line',
    data: data,
    options: {}
  };

  // === include 'setup' then 'config' above ===

  var myChart = new Chart(
    document.getElementById('myChart'),
    config
  );