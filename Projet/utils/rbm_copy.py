import numpy as np

class RBM():
    def __init__(self, p, q):
        """
        Args:
            p (int): input size (number of visible variables)
            q (int): output size (number of latent variables)
        """
        self.p = p
        self.q = q
        self.a = np.zeros(p)
        self.b = np.zeros(q)
        self.W = np.random.randn(p, q) * np.sqrt(0.01)

    def entree_sortie(self, X):
        """
        Args:
            X (np.array): array of size n*p
        Return:
            (np.array) array of size n*q
        """
        sortie = 1 / (1 + np.exp(-(X @ self.W + self.b)))
        return sortie

    def sortie_entree(self, H):
        """
        Args:
            H (np.array): array of size n*q
        Return:
            (np.array) array of size n*p
        """
        entree = 1 / (1 + np.exp(-(H @ self.W.T + self.a)))
        return entree

    def train_RBM(self, X, n_epochs, lr, batch_size):
        """
        Learning the parameters with Contrastive-Divergence-1 algorithm
        Args:
            X (np.array): size n*p
            lr (float): learning_rate
            batch_size (int): batch_size
            n_epochs (int): number of epochs
        """
        errors = []
        for k in range(n_epochs):
            np.random.shuffle(X)

            for l in range(0, X.shape[0], batch_size):
                X_batch = X[l:min(X.shape[0], l + batch_size)]
                tb = X_batch.shape[0]

                # Forward
                v_0 = X_batch  # size tb*p
                p_h_v_0 = self.entree_sortie(v_0)  # size tb*q
                h_0 = (np.random.rand(tb, self.q) < p_h_v_0) * 1  # size tb*q
                # Backward
                p_v_h_0 = self.sortie_entree(h_0)  # size tb*p
                v_1 = (np.random.rand(tb, self.p) < p_v_h_0) * 1  # size tb*p
                p_h_v_1 = self.entree_sortie(v_1)

                # Calcul des gradients
                grad_a = np.sum(v_0 - v_1, axis=0)  # size p
                grad_b = np.sum(p_h_v_0 - p_h_v_1, axis=0)  # size q
                grad_W = v_0.T @ p_h_v_0 - v_1.T @ p_h_v_1  # size p*q

                # Update parameters
                self.W = self.W + (lr / tb) * grad_W
                self.a = self.a + (lr / tb) * grad_a
                self.b = self.b + (lr / tb) * grad_b

            diff = abs(v_0 - v_1)
            mse = np.sum(diff) / diff.shape[0]
            errors.append(mse)
            # print(f"Mean Square Error at iteration {k} : ", mse)
        return errors

    def generer_image(self, nb_iter_gibbs, nb_image):
        p = self.a.size
        q = self.b.size
        generated_images = []

        for image in range(nb_image):
            v = (np.random.rand(p) < 0.5) * 1  # visible state
            for i in range(nb_iter_gibbs):
                h = (np.random.rand(q) < self.entree_sortie(v)) * 1  # hidden state
                v = (np.random.rand(p) < self.sortie_entree(h)) * 1

            generated_images.append(v)

        return generated_images