document.addEventListener('DOMContentLoaded', loadProducts);

async function loadProducts() {
    const container = document.getElementById('product-list');
    container.innerHTML = '<p>Loading products...</p>';

    try {
        const response = await fetch('/api/products/?available=true&ordering=-created_at');
        if (!response.ok) throw new Error('Failed to load products');

        const products = await response.json();

        if (products.length === 0) {
            container.innerHTML = '<p>No products available at the moment.</p>';
            return;
        }

        container.innerHTML = '';

        products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';

            const image = product.image
                ? `<img src="${product.image}" alt="${product.name}" class="product-image">`
                : '<div class="product-image" style="background:#eee;display:flex;align-items:center;justify-content:center;">No image</div>';

            card.innerHTML = `
                ${image}
                <div class="product-info">
                    <h3>${product.name}</h3>
                    <p class="price">$${parseFloat(product.price).toFixed(2)}</p>
                    <p class="${product.in_stock ? 'stock' : 'out-of-stock'}">
                        ${product.in_stock ? 'In Stock' : 'Out of Stock'}
                    </p>
                    <p>${product.description.substring(0, 80)}${product.description.length > 80 ? '...' : ''}</p>
                </div>
            `;

            container.appendChild(card);
        });
    } catch (error) {
        container.innerHTML = `<p style="color:red;">Error loading products: ${error.message}</p>`;
        console.error(error);
    }
}