const jsonServer = require('json-server');

const app = jsonServer.create();

const middlewares = jsonServer.defaults();
app.use(middlewares);

const router = jsonServer.router('data/data_7-K16813-1026.json');
app.use(router);

app.listen(3000, () => {
  console.log('JSON Server is running');
});
