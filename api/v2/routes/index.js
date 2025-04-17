/**
 * API Routes Index
 * 
 * Tập hợp tất cả routes cho API v2
 */

const express = require('express');
const router = express.Router();

// Import các routes
const rootAgentRoutes = require('./root-agent');
const batCucLinhSoRoutes = require('./bat-cuc-linh-so');
const userRoutes = require('./user');
const paymentRoutes = require('./payment');

// Root route
router.get('/', (req, res) => {
  res.json({
    message: 'Phong Thủy Số API v2',
    version: '2.0.0',
    status: 'active',
    endpoints: [
      '/agent',
      '/bat-cuc-linh-so',
      '/user',
      '/payment'
    ]
  });
});

// Mount các routes
router.use('/agent', rootAgentRoutes);
router.use('/bat-cuc-linh-so', batCucLinhSoRoutes);
router.use('/user', userRoutes);
router.use('/payment', paymentRoutes);

module.exports = router; 