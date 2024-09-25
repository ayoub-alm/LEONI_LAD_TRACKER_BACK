INSERT INTO `users` (`id`, `username`, `matriculate`, `password`, `role`, `created_at`, `deleted_at`, `updated_at`, `created_by`) VALUES
(1, 'leoni', '111213', '111213', 'admin', NULL, NULL, NULL, NULL);


INSERT INTO `posts`(`id`, `name`, `created_at`, `deleted_at`, `updated_at`, `created_by`) VALUES
(1, 'PTA', '2024-05-30 19:00:59', NULL, '2024-05-30 19:01:04', NULL),
(2, 'BOL 1', '2024-05-30 19:00:59', NULL, '2024-05-30 19:01:04', NULL),
(3, 'BOL 2', '2024-05-30 19:00:59', NULL, '2024-05-30 19:01:04', NULL),
(4, 'packaging', '2024-05-30 19:00:59', NULL, '2024-05-30 19:01:04', NULL);


INSERT INTO `fields`(`id`, `name`, `post_id`, `created_at`, `deleted_at`, `updated_at`, `created_by`) VALUES
(1, 'Counter', 1, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(2, 'Harness reference', 1, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(3, 'Counter', 2, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(4, 'Harness reference', 2, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(5, 'Counter', 3, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(6, 'Harness reference', 3, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(7, 'Box barcode', 4, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(8, 'Box harness-reference', 4, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(9, 'Box size', 2, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(10, 'Box size', 4, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL),
(11, 'Box quantity', 4, '2024-05-30 19:04:42', NULL, '2024-05-30 19:04:42', NULL);


