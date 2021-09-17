$(function(){
    var IMP=window.IMP;
    IMP.init('imp18325231')
    $('.order-form').on('submit', function(e){
        var amount = parseFloat($('.order-form input[name="amount"]').val().replace(',',''));
        var type=$('.order-form input[name="type"]:checkout').val();
        var order_id = AjaxCreateOrder(e);
        if(order_id==False){
            alert('Order Failed. Try again');
            return false;
        }

        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);

        if(merchant_id!==''){
            IMP.request_pay({
                merchant_uid:merchant_id,
                name:'Order Product',
                buyer_name:$('input[name="first_name"]').val()+""+$('input[name="last_name"]').val(),
                buyer_email:$('input[name="email"]').val(),
                amount:amount
            }, function(req){
                if(req.success){
                    var msg = "Payment Completed";
                    msg += "Order id : " + req.imp_uid;
                    // Message after payment
                    ImpTransaction(e, order_id, req.merchant_uid, req.imp_uid, req.paid_amount);
                } else{
                    var msg = "Payment Failed";
                    msg += "Error : " + req.error_msg;
                    console.log(msg);
                }
            });
        }
        return false;
    });
});