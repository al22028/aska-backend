const faker = require('faker');
const fs = require('fs');
const path = require('node:path');

function generatePage(identification, index) {
    return {
        id: identification,
        index: `${identification.split('-')[0]}-${index}-${parseInt(identification.split('-')[0]) + (index - 1)}`,
        src: `https://images.u10.teba-saki.net/${identification.split('-')[0]}-${identification.split('-')[1]}-${identification.split('-')[2]}/${identification.split('-')[3]}.png`,
        status: "PREPROCESSED",
        updatedAt: faker.date.past().toISOString(),
        createdAt: faker.date.past().toISOString()
    };
}

function generateDocument(id, pageCount) {
    let pages = [];
    for (let i = 1; i <= pageCount; i++) {
        const pageId = `${id}-${i}`;
        pages.push(generatePage(pageId, i));
    }

    return {
        id: id,
        title: faker.lorem.words(),
        description: faker.lorem.sentence(),
        updatedAt: faker.date.past().toISOString(),
        createdAt: faker.date.past().toISOString(),
        pages: pages
    };
}

async function save_json(identificatoin, num_pages) {
    const dummyData = generateDocument(identificatoin, num_pages);
    const jsonData = JSON.stringify(dummyData, null, 2);

    await fs.promises.mkdir('data', { recursive: true })
    file_path = path.join(process.cwd(), 'data', `data_${identificatoin}.json`);
    console.log(file_path);
    fs.writeFile(file_path, jsonData, (err) => {
        if(err) {
            console.log('Error');
            return
        }
    });
}

module.exports = { save_json };
