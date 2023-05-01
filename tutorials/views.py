from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import time
from tutorials import bybit
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer


@api_view(['GET'])
def tutorial_list(request):
    if request.method == 'GET':

        if (request.GET.get('operation_type', '') is not None or request.GET.get('operation_type', '') != ''):
            operation_type = request.GET.get('operation_type', '')
            bybitti = bybit.Bybit()
            if (operation_type == 'balance'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                coin = request.GET.get('coin', '')

                availabaleBalance = bybitti.available_balance(api_key=api_key, api_secret=api_secret,
                                                              coin=coin)
                if availabaleBalance != '' or availabaleBalance is not None:
                    d = {'balance': str(availabaleBalance)}

                    return JsonResponse(d, status=status.HTTP_200_OK)

            if (operation_type == 'long'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                leverage = request.GET.get('leverage', '')
                leverage_float = float(leverage)
                amount_perc = request.GET.get('amount_perc', '')
                amount_perc_float = float(amount_perc)
                price = request.GET.get('price', '')
                price_float = float(price)
                take_profit = request.GET.get('take_profit', '')
                stop_loss = request.GET.get('stop_loss', '')

                availabaleBalance = bybitti.available_balance(api_key=api_key, api_secret=api_secret,
                                                              coin="USDT")
                availabaleBalance_float = float(availabaleBalance)
                amount = (availabaleBalance_float * (amount_perc_float / 100) * leverage_float * (
                            1 - (0.0016 * 2))) / price_float
                amount = round(amount, 6)
                print("dopo amount")
                print(amount)

                mode = bybitti.setOneWay(api_key=api_key, api_secret=api_secret, symbol=symbol)

                leverage = bybitti.set_leverage(api_key=api_key, api_secret=api_secret, symbol=symbol,
                                                leverage=leverage)

                long = bybitti.long(api_key=api_key, api_secret=api_secret, symbol=symbol, qty=str(amount),
                                    price=price, take_profit=take_profit, stop_loss=stop_loss)
                return JsonResponse(long)

            if (operation_type == 'short'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                leverage = request.GET.get('leverage', '')
                leverage_float = float(leverage)
                amount_perc = request.GET.get('amount_perc', '')
                amount_perc_float = float(amount_perc)
                price = request.GET.get('price', '')
                price_float = float(price)
                take_profit = request.GET.get('take_profit', '')
                stop_loss = request.GET.get('stop_loss', '')

                availabaleBalance = bybitti.available_balance(api_key=api_key, api_secret=api_secret,
                                                              coin="USDT")
                availabaleBalance_float = float(availabaleBalance)
                amount = (availabaleBalance_float * (amount_perc_float / 100) * leverage_float * (
                        1 - (0.0016 * 2))) / price_float
                amount = round(amount, 6)

                mode = bybitti.setOneWay(api_key=api_key, api_secret=api_secret, symbol=symbol)

                leverage = bybitti.set_leverage(api_key=api_key, api_secret=api_secret, symbol=symbol,
                                                leverage=leverage)
                short = bybitti.short(api_key=api_key, api_secret=api_secret, symbol=symbol, qty=str(amount),
                                      price=price, take_profit=take_profit, stop_loss=stop_loss)
                return JsonResponse(short)

            if operation_type == 'updateTPOrder.short':
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                take_profit = request.GET.get('take_profit', '')

                updateTPOrder = bybitti.updateTPOrderShort(api_key=api_key, api_secret=api_secret, symbol=symbol
                                                           , take_profit=take_profit)
                return JsonResponse(updateTPOrder)

            if operation_type == 'updateTPOrder.long':
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                take_profit = request.GET.get('take_profit', '')

                updateTPOrder = bybitti.updateTPOrderLong(api_key=api_key, api_secret=api_secret, symbol=symbol
                                                          , take_profit=take_profit)
                return JsonResponse(updateTPOrder)

            if (operation_type == 'updateSLOrder.premium'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                stop_loss = request.GET.get('stop_loss', '')

                updateSLOrder = bybitti.updateSLOrder(api_key=api_key, api_secret=api_secret, symbol=symbol
                                                      , stop_loss=stop_loss)
                return JsonResponse(updateSLOrder)

            if (operation_type == 'updateSLOrder.basic'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')
                stop_loss = request.GET.get('stop_loss', '')

                updateSLOrder = bybitti.updateSLOrder(api_key=api_key, api_secret=api_secret, symbol=symbol
                                                      , stop_loss=stop_loss)
                return JsonResponse(updateSLOrder)

            if (operation_type == 'cancelAllOrders'):
                api_key = request.GET.get('api_key', '')
                api_secret = request.GET.get('api_secret', '')
                symbol = request.GET.get('symbol', '')

                cancelAllOrders = bybitti.cancelAllOrders(api_key=api_key, api_secret=api_secret, symbol=symbol)
                return JsonResponse(cancelAllOrders)

        # print(short)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)

    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


