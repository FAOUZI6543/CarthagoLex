export function GPTCard(gpt) {
  const card = document.createElement('article');
  card.className = 'gpt-card';
  card.innerHTML = `
    <h3><a href="/gpts/${gpt.slug}">${gpt.name}</a></h3>
    <p>${gpt.description}</p>
  `;
  return card;
}
